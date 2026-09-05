#!/usr/bin/env python3
"""Watchdog de cotas Groq Free-tier. Key só via env GROQ_API_KEY. Sem spend."""
from __future__ import annotations

import json
import os
import ssl
import sys
import http.client

DEFAULT_MODEL = "qwen/qwen3.6-27b"
RPD_STOP_USED_PCT = 80.0
TPM_FLOOR = 400


def headers(key: str) -> dict:
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": "groq-python/1.0",
        "Accept": "application/json",
        "Connection": "close",
    }


def probe(key: str, model: str) -> dict:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "ok"}],
        "max_tokens": 4,
    }
    if model.startswith("qwen/"):
        payload["reasoning_effort"] = "none"
    body = json.dumps(payload).encode()
    conn = http.client.HTTPSConnection(
        "api.groq.com", timeout=60, context=ssl.create_default_context()
    )
    conn.request("POST", "/openai/v1/chat/completions", body=body, headers=headers(key))
    resp = conn.getresponse()
    status = resp.status
    raw = {k.lower(): v for k, v in resp.getheaders()}
    text = resp.read().decode("utf-8", "replace")
    conn.close()

    lim = float(raw.get("x-ratelimit-limit-requests") or 0)
    rem = float(raw.get("x-ratelimit-remaining-requests") or 0)
    tpm = float(raw.get("x-ratelimit-remaining-tokens") or 0)
    used = ((1.0 - rem / lim) * 100.0) if lim > 0 else None

    decision = "OK"
    reasons = []
    if status == 429:
        decision = "STOP"
        reasons.append(f"HTTP_429 retry_after={raw.get('retry-after')}")
    if used is not None and used >= RPD_STOP_USED_PCT:
        decision = "STOP"
        reasons.append(f"RPD_HIGH used_pct={used:.1f}")
    if tpm and tpm < TPM_FLOOR:
        decision = "STOP"
        reasons.append(f"TPM_CRITICAL rem={tpm}")
    if status >= 400 and status != 429:
        decision = "ERROR"
        reasons.append(f"HTTP_{status}")

    return {
        "decision": decision,
        "reasons": reasons,
        "http": status,
        "model": model,
        "rpd_limit": raw.get("x-ratelimit-limit-requests"),
        "rpd_rem": raw.get("x-ratelimit-remaining-requests"),
        "tpm_limit": raw.get("x-ratelimit-limit-tokens"),
        "tpm_rem": raw.get("x-ratelimit-remaining-tokens"),
        "rpd_used_pct": round(used, 2) if used is not None else None,
        "region": raw.get("x-groq-region"),
        "retry_after": raw.get("retry-after"),
        "body_snip": text[:180] if status >= 400 else None,
    }


if __name__ == "__main__":
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise SystemExit("Defina GROQ_API_KEY no ambiente (nunca hardcode).")
    model = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL
    out = probe(key, model)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    raise SystemExit(0 if out["decision"] == "OK" else 2)
