---
produto: Structured Outputs strict (json_schema)
preco_BRL: 10
fontes: console.groq.com/docs/structured-outputs, /models, /rate-limits
---

# Groq Free-tier: Structured Outputs (`json_schema` + `strict`)

Diferença vs `JSON-MODE.md`: aqui é **`response_format.type=json_schema`** com `strict: true` (constrained decoding), não só `json_object`.

## Chamada (chat completions)

```json
{
  "model": "openai/gpt-oss-20b",
  "messages": [
    {"role": "system", "content": "Extract a tiny ticket."},
    {"role": "user", "content": "Bug: login 500 on /api/me. Priority high."}
  ],
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "ticket",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "title": {"type": "string"},
          "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
          "component": {"type": "string"}
        },
        "required": ["title", "priority", "component"],
        "additionalProperties": false
      }
    }
  },
  "max_tokens": 256
}
```

## Regras `strict: true`

- Todos os campos em `required`.
- Objetos com `additionalProperties: false`.
- Opcionais: use union `["string","null"]` e ainda liste em `required` ([docs](https://console.groq.com/docs/structured-outputs)).

## Modelos Free com strict

- `openai/gpt-oss-20b`, `openai/gpt-oss-120b`, `qwen/qwen3.8-27b`

Streaming + tool use **não** com Structured Outputs. Sem inventar RPM — leia headers / [rate-limits](https://console.groq.com/docs/rate-limits).

Script: `structured_schema.py`.

## CTA

https://ziuluiziul.github.io/groq-round1-offer/ — tip **R$10** / kit **R$20**.
