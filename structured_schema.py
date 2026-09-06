#!/usr/bin/env python3
"""Structured Outputs strict json_schema (openai/gpt-oss-20b). Key: GROQ_API_KEY."""
from __future__ import annotations

import http.client
import json
import os
import ssl
import sys

MODEL = "openai/gpt-oss-20b"
RPD_STOP_USED_PCT = 80.0
TPM_FLOOR = 400

SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "priority": {
            "type": "string",
            "enum": ["low", "medium", "high", "critical"],
        },
        "component": {"type": "string"},
    },
    "required": ["title", "priority", "component"],
    "additionalProperties": False,
}


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


def chat_schema(key: str) -> dict:
    body = json.dumps(
        {
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "Extract a support ticket. Follow the JSON schema exactly.",
                },
                {
                    "role": "user",
                    "content": "Bug: login returns 500 on /api/me after deploy. Priority high. Component auth.",
                },
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "ticket",
                    "strict": True,
                    "schema": SCHEMA,
                },
            },
            "temperature": 0,
            "max_tokens": 256,
        }
    ).encode()
    ctx = ssl.create_default_context()
    conn = http.client.HTTPSConnection("api.groq.com", context=ctx, timeout=60)
    conn.request("POST", "/openai/v1/chat/completions", body=body, headers=headers(key))
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
    out = chat_schema(key)
    meta = out["meta"]
    data = out["data"]
    content = ""
    parsed = None
    try:
        content = (data.get("choices") or [{}])[0].get("message", {}).get("content") or ""
        parsed = json.loads(content)
    except Exception:
        parsed = None
    ok = (
        meta["http"] == 200
        and isinstance(parsed, dict)
        and set(SCHEMA["required"]).issubset(parsed.keys())
    )
    print(
        json.dumps(
            {
                "ok": ok,
                "http": meta["http"],
                "model": MODEL,
                "parsed": parsed,
                "rpd_remaining": meta["rpd_remaining"],
                "tpm_remaining": meta["tpm_remaining"],
                "region": meta["region"],
                "stop": meta["stop"],
                "error": data.get("error") if isinstance(data, dict) else None,
            },
            indent=2,
        )
    )
    if meta["stop"]:
        return 3
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
