#!/usr/bin/env python3
"""Streaming SSE chat Groq Free-tier. Key só via env GROQ_API_KEY. Sem spend."""
from __future__ import annotations

import http.client
import json
import os
import ssl
import sys
import time


def headers(key: str) -> dict:
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": "groq-python/1.0",
    }


def stream_chat(key: str, model: str, prompt: str, max_tokens: int = 256) -> dict:
    body = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.2,
            "stream": True,
        }
    ).encode()
    conn = http.client.HTTPSConnection(
        "api.groq.com", timeout=120, context=ssl.create_default_context()
    )
    conn.request("POST", "/openai/v1/chat/completions", body=body, headers=headers(key))
    resp = conn.getresponse()
    meta = {
        "status": resp.status,
        "rpd_rem": resp.getheader("x-ratelimit-remaining-requests"),
        "tpm_rem": resp.getheader("x-ratelimit-remaining-tokens"),
        "retry_after": resp.getheader("retry-after"),
    }
    if resp.status == 429:
        conn.close()
        wait = float(meta["retry_after"] or 5)
        return {"ok": False, "meta": meta, "error": "429", "sleep": wait}
    if resp.status != 200:
        err = resp.read().decode(errors="replace")[:400]
        conn.close()
        return {"ok": False, "meta": meta, "error": err}

    parts: list[str] = []
    while True:
        line = resp.readline()
        if not line:
            break
        s = line.decode(errors="replace").strip()
        if not s or not s.startswith("data:"):
            continue
        payload = s[5:].strip()
        if payload == "[DONE]":
            break
        try:
            chunk = json.loads(payload)
        except json.JSONDecodeError:
            continue
        delta = (chunk.get("choices") or [{}])[0].get("delta") or {}
        # gpt-oss may stream "reasoning" first; prefer visible content
        piece = delta.get("content")
        if piece is None and not parts:
            # only surface reasoning if no content yet (debug-friendly)
            piece = None
        if piece:
            parts.append(piece)
            sys.stdout.write(piece)
            sys.stdout.flush()
    conn.close()
    print()
    return {"ok": True, "meta": meta, "text": "".join(parts)}


def main() -> None:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise SystemExit("Defina GROQ_API_KEY no ambiente (nunca hardcode).")
    model = os.environ.get("GROQ_MODEL", "qwen/qwen3.6-27b")
    prompt = " ".join(sys.argv[1:]) or "Diga oi em uma frase curta."
    result = stream_chat(key, model, prompt)
    if not result.get("ok") and result.get("error") == "429":
        time.sleep(result.get("sleep") or 5)
        result = stream_chat(key, model, prompt)
    print(json.dumps({"ok": result.get("ok"), "meta": result.get("meta")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
