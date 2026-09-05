#!/usr/bin/env python3
"""Tool calling local Groq Free-tier. Key só via env GROQ_API_KEY. Sem spend."""
from __future__ import annotations

import http.client
import json
import os
import ssl
import sys

MODEL_DEFAULT = "qwen/qwen3.6-27b"
RPD_STOP_USED_PCT = 80.0
TPM_FLOOR = 400

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Multiplica dois inteiros",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "primeiro fator"},
                    "b": {"type": "integer", "description": "segundo fator"},
                },
                "required": ["a", "b"],
            },
        },
    }
]


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


def chat(key: str, messages: list, model: str) -> tuple[dict, dict]:
    body = json.dumps(
        {
            "model": model,
            "messages": messages,
            "tools": TOOLS,
            "tool_choice": "auto",
            "max_tokens": 256,
            "temperature": 0,
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
    }
    stop = risk_stop(resp)
    conn.close()
    if stop:
        raise SystemExit(f"STOP API: {stop} meta={meta}")
    if resp.status != 200:
        raise SystemExit(f"HTTP {resp.status}: {raw.decode(errors='replace')[:400]}")
    return json.loads(raw), meta


def run_tool(name: str, args: dict) -> str:
    if name == "multiply":
        return str(int(args["a"]) * int(args["b"]))
    return json.dumps({"error": f"unknown tool {name}"})


def main() -> None:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise SystemExit("Defina GROQ_API_KEY no ambiente (nunca hardcode).")
    model = os.environ.get("GROQ_MODEL", MODEL_DEFAULT)
    user = " ".join(sys.argv[1:]) or "Quanto é 21*2? Use a ferramenta multiply."
    messages = [{"role": "user", "content": user}]
    data, meta1 = chat(key, messages, model)
    msg = data["choices"][0]["message"]
    tool_calls = msg.get("tool_calls") or []
    if not tool_calls:
        print(json.dumps({"meta": meta1, "content": msg.get("content")}, ensure_ascii=False, indent=2))
        return
    messages.append(
        {
            "role": "assistant",
            "content": msg.get("content"),
            "tool_calls": tool_calls,
        }
    )
    for tc in tool_calls:
        fn = tc["function"]
        args = json.loads(fn.get("arguments") or "{}")
        result = run_tool(fn["name"], args)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tc["id"],
                "name": fn["name"],
                "content": result,
            }
        )
    data2, meta2 = chat(key, messages, model)
    final = data2["choices"][0]["message"].get("content")
    print(
        json.dumps(
            {
                "meta_round1": meta1,
                "meta_round2": meta2,
                "tool_calls": tool_calls,
                "final": final,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
