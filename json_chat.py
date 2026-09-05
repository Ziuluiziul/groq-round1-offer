#!/usr/bin/env python3
"""JSON mode helper Groq Free-tier. Key só via env GROQ_API_KEY. Sem spend."""
from __future__ import annotations

import http.client
import json
import os
import re
import ssl
import sys


def headers(key: str) -> dict:
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": "groq-python/1.0",
    }


def strip_fences(text: str) -> str:
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*", "", t, flags=re.I)
    t = re.sub(r"\s*```$", "", t)
    t = re.sub(r"<think>[\s\S]*?</think>", "", t, flags=re.I).strip()
    return t


def json_chat(key: str, model: str, user: str, max_tokens: int = 256) -> dict:
    body = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "system", "content": "Responda apenas JSON válido."},
                {"role": "user", "content": user},
            ],
            "max_tokens": max_tokens,
            "temperature": 0,
            "response_format": {"type": "json_object"},
        }
    ).encode()
    conn = http.client.HTTPSConnection(
        "api.groq.com", timeout=90, context=ssl.create_default_context()
    )
    conn.request("POST", "/openai/v1/chat/completions", body=body, headers=headers(key))
    resp = conn.getresponse()
    raw = resp.read()
    meta = {
        "status": resp.status,
        "rpd_rem": resp.getheader("x-ratelimit-remaining-requests"),
        "tpm_rem": resp.getheader("x-ratelimit-remaining-tokens"),
        "retry_after": resp.getheader("retry-after"),
    }
    conn.close()
    if resp.status != 200:
        return {"ok": False, "meta": meta, "error": raw.decode(errors="replace")[:400]}
    content = json.loads(raw)["choices"][0]["message"].get("content") or ""
    cleaned = strip_fences(content)
    try:
        obj = json.loads(cleaned)
    except json.JSONDecodeError as e:
        return {"ok": False, "meta": meta, "error": f"JSONDecodeError: {e}", "raw": cleaned[:300]}
    return {"ok": True, "meta": meta, "data": obj}


def main() -> None:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise SystemExit("Defina GROQ_API_KEY no ambiente (nunca hardcode).")
    model = os.environ.get("GROQ_MODEL", "openai/gpt-oss-20b")
    user = " ".join(sys.argv[1:]) or '{"schema":{"ok":"bool","msg":"string"},"task":"ping"}'
    print(json.dumps(json_chat(key, model, user), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
