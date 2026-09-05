#!/usr/bin/env python3
"""ROUND1 smoke — Groq Free-tier. Key só via env."""
import json, os, http.client, ssl
key = os.environ["GROQ_API_KEY"]
payload = json.dumps({
    "model": "qwen/qwen3.6-27b",
    "messages": [{"role": "user", "content": "ping em uma palavra"}],
    "max_tokens": 8,
}).encode()
conn = http.client.HTTPSConnection("api.groq.com", timeout=90, context=ssl.create_default_context())
conn.request("POST", "/openai/v1/chat/completions", body=payload, headers={
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "User-Agent": "groq-python/1.0",
    "Connection": "close",
})
r = conn.getresponse()
print("HTTP", r.status)
print("RPD_rem", r.getheader("x-ratelimit-remaining-requests"))
print(r.read().decode()[:500])
conn.close()
