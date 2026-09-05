#!/usr/bin/env python3
"""Failover multi-modelo Groq Free-tier. Key só via env GROQ_API_KEY. Sem spend."""
from __future__ import annotations

import json
import os
import ssl
import sys
import time
import http.client

# Ordem Free chat (docs rate-limits + deprecations 2026-08-16)
MODELS = [
    "qwen/qwen3.6-27b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-120b",
]

RPD_STOP_USED_PCT = 80.0  # stop if used >= 80% of daily requests
TPM_FLOOR = 400           # abort if remaining TPM critically low


def _headers(key: str) -> dict:
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": "groq-python/1.0",
        "Accept": "application/json",
        "Connection": "close",
    }


def _risk_stop(raw: dict) -> str | None:
    try:
        lim = float(raw.get("x-ratelimit-limit-requests") or 0)
        rem = float(raw.get("x-ratelimit-remaining-requests") or 0)
        if lim > 0:
            used = (1.0 - rem / lim) * 100.0
            if used >= RPD_STOP_USED_PCT:
                return f"RPD_HIGH_RISK used_pct={used:.1f} rem={rem}/{lim}"
        tpm = float(raw.get("x-ratelimit-remaining-tokens") or 99999)
        if tpm < TPM_FLOOR:
            return f"TPM_CRITICAL rem={tpm}"
    except Exception:
        return None
    return None


def once(key: str, model: str, message: str, max_tokens: int = 256):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": message}],
        "max_tokens": max_tokens,
    }
    if model.startswith("qwen/"):
        payload["reasoning_effort"] = "none"
    body = json.dumps(payload).encode()
    conn = http.client.HTTPSConnection(
        "api.groq.com", timeout=90, context=ssl.create_default_context()
    )
    conn.request("POST", "/openai/v1/chat/completions", body=body, headers=_headers(key))
    resp = conn.getresponse()
    status = resp.status
    raw = {k.lower(): v for k, v in resp.getheaders()}
    text = resp.read().decode("utf-8", "replace")
    conn.close()
    return status, raw, text


def chat(message: str, max_tokens: int = 256) -> dict:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise SystemExit("Defina GROQ_API_KEY no ambiente (nunca hardcode).")

    last = {}
    for model in MODELS:
        status, raw, text = once(key, model, message, max_tokens)
        risk = _risk_stop(raw)
        meta = {
            "model": model,
            "http": status,
            "rpd_rem": raw.get("x-ratelimit-remaining-requests"),
            "tpm_rem": raw.get("x-ratelimit-remaining-tokens"),
            "region": raw.get("x-groq-region"),
        }
        if risk:
            meta["stop"] = risk
            return meta

        if status == 429:
            wait = float(raw.get("retry-after") or 2)
            time.sleep(min(max(wait, 0), 60))
            last = {**meta, "error": "429", "retry_after": wait}
            continue  # próximo modelo

        if status >= 400:
            last = {**meta, "error_body": text[:300]}
            continue

        try:
            data = json.loads(text)
            content = ((data.get("choices") or [{}])[0].get("message") or {}).get("content")
            usage = data.get("usage") or {}
        except Exception:
            content, usage = text[:500], {}
        return {**meta, "content": content, "usage": usage}

    return last or {"error": "all_models_failed"}


if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) or "ping em uma palavra"
    out = chat(msg, max_tokens=64)
    print(json.dumps(out, ensure_ascii=False, indent=2)[:2000])
