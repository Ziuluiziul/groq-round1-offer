#!/usr/bin/env python3
"""Responses API mini (openai/gpt-oss-20b). Key: GROQ_API_KEY. Free-tier."""
from __future__ import annotations

import http.client
import json
import os
import ssl
import sys

MODEL = "openai/gpt-oss-20b"
RPD_STOP_USED_PCT = 80.0
TPM_FLOOR = 400


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


def responses_create(key: str) -> dict:
    body = json.dumps(
        {
            "model": MODEL,
            "input": "One short sentence: why use GroqCloud free-tier for chat APIs?",
            "reasoning": {"effort": "low"},
            "max_output_tokens": 96,
        }
    ).encode()
    ctx = ssl.create_default_context()
    conn = http.client.HTTPSConnection("api.groq.com", context=ctx, timeout=90)
    conn.request("POST", "/openai/v1/responses", body=body, headers=headers(key))
    resp = conn.getresponse()
    raw = resp.read().decode()
    stop = risk_stop(resp)
    meta = {
        "http": resp.status,
        "rpd_remaining": resp.getheader("x-ratelimit-remaining-requests"),
        "tpm_remaining": resp.getheader("x-ratelimit-remaining-tokens"),
        "region": resp.getheader("x-groq-region"),
        "stop": stop,
    }
    conn.close()
    try:
        data = json.loads(raw)
    except Exception:
        data = {"raw": raw[:400]}
    return {"meta": meta, "data": data}


def main() -> int:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        print("GROQ_API_KEY missing", file=sys.stderr)
        return 2
    out = responses_create(key)
    meta = out["meta"]
    data = out["data"]
    text = data.get("output_text") or ""
    if not text and isinstance(data.get("output"), list):
        for item in data["output"]:
            if item.get("type") == "message":
                for c in item.get("content") or []:
                    if c.get("type") in ("output_text", "text"):
                        text += c.get("text") or ""
    print(
        json.dumps(
            {
                "ok": meta["http"] == 200 and bool(text.strip()),
                "http": meta["http"],
                "model": MODEL,
                "output_len": len(text),
                "preview": text[:160].replace("\n", " "),
                "rpd_remaining": meta["rpd_remaining"],
                "tpm_remaining": meta["tpm_remaining"],
                "region": meta["region"],
                "stop": meta["stop"],
                "error": (data.get("error") if isinstance(data, dict) else None),
            },
            indent=2,
        )
    )
    if meta["stop"]:
        return 3
    return 0 if meta["http"] == 200 and text.strip() else 1


if __name__ == "__main__":
    raise SystemExit(main())
