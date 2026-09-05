#!/usr/bin/env python3
"""Compound-mini one-shot (server tools). Key: GROQ_API_KEY. Free-tier RPD 250."""
from __future__ import annotations

import http.client
import json
import os
import ssl
import sys

MODEL = "groq/compound-mini"
RPD_STOP_USED_PCT = 80.0
TPM_FLOOR = 1000  # compound TPM is 70K; keep a soft floor


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


def ask(key: str, prompt: str) -> dict:
    body = json.dumps(
        {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode()
    ctx = ssl.create_default_context()
    conn = http.client.HTTPSConnection("api.groq.com", context=ctx, timeout=120)
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
        raise SystemExit(f"HTTP {resp.status}: {raw[:400]!r}")
    data = json.loads(raw)
    msg = (data.get("choices") or [{}])[0].get("message", {})
    return {
        "meta": meta,
        "content": (msg.get("content") or "")[:500],
        "executed_tools": msg.get("executed_tools"),
        "usage": data.get("usage"),
    }


def main() -> None:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise SystemExit("set GROQ_API_KEY")
    # Keep prompt computation-local to avoid external web dependency flakiness
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Compute 17*19 using code execution. Reply with the number only."
    print(json.dumps(ask(key, prompt), ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
