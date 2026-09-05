#!/usr/bin/env python3
"""Prompt caching demo (openai/gpt-oss-20b). Key: GROQ_API_KEY. Free-tier."""
from __future__ import annotations

import http.client
import json
import os
import ssl
import sys

MODEL = "openai/gpt-oss-20b"
RPD_STOP_USED_PCT = 80.0
TPM_FLOOR = 400

SYSTEM = (
    "You are a concise technical assistant for Groq Free-tier integrations. "
    "Answer in one short sentence. Always prefer official console.groq.com/docs. "
    "Never invent RPM numbers. Keep answers under 40 words. "
    "This static prefix exists to demonstrate prompt caching prefix matching."
)


def headers(key: str) -> dict:
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": "groq-python/1.0",
        "Connection": "close",
    }


def risk_stop(resp) -> str | None:
    try:
        lim = float(resp.getheader("x-ratelimit-limit-requests") or 0)
        rem = float(resp.getheader("x-ratelimit-remaining-requests") or 0)
        if lim > 0 and (1.0 - rem / lim) * 100.0 >= RPD_STOP_USED_PCT:
            return f"RPD used>={RPD_STOP_USED_PCT}%"
        tpm = float(resp.getheader("x-ratelimit-remaining-tokens") or 99999)
        if tpm < TPM_FLOOR:
            return f"TPM remaining critical ({tpm})"
    except Exception:
        return None
    return None


def chat(key: str, user: str) -> dict:
    body = json.dumps(
        {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": user},
            ],
            "temperature": 0,
            "max_tokens": 256,
        }
    ).encode()
    ctx = ssl.create_default_context()
    conn = http.client.HTTPSConnection("api.groq.com", context=ctx, timeout=60)
    conn.request("POST", "/openai/v1/chat/completions", body=body, headers=headers(key))
    resp = conn.getresponse()
    raw = resp.read()
    stop = risk_stop(resp)
    meta = {
        "http": resp.status,
        "rpd_remaining": resp.getheader("x-ratelimit-remaining-requests"),
        "tpm_remaining": resp.getheader("x-ratelimit-remaining-tokens"),
        "stop": stop,
    }
    conn.close()
    if stop:
        raise SystemExit(f"STOP: {stop} meta={meta}")
    if resp.status != 200:
        raise SystemExit(f"HTTP {resp.status}: {raw[:300]!r}")
    data = json.loads(raw)
    usage = data.get("usage") or {}
    details = usage.get("prompt_tokens_details") or {}
    msg = (data.get("choices") or [{}])[0].get("message", {})
    content = msg.get("content") or ""
    if not content and msg.get("reasoning"):
        content = "(reasoning-only) " + str(msg.get("reasoning"))[:160]
    return {
        "meta": meta,
        "content": content,
        "prompt_tokens": usage.get("prompt_tokens"),
        "cached_tokens": details.get("cached_tokens", 0),
    }


def main() -> None:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise SystemExit("set GROQ_API_KEY")
    q1 = sys.argv[1] if len(sys.argv) > 1 else "What is prompt caching on Groq?"
    q2 = sys.argv[2] if len(sys.argv) > 2 else "Where do I read Free rate limits?"
    for q in (q1, q2):
        out = chat(key, q)
        print(json.dumps({"q": q, **out}, ensure_ascii=False))


if __name__ == "__main__":
    main()
