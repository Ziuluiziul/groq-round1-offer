---
produto: Tool calling local Groq Free
preco_BRL: 20
fontes: console.groq.com/docs/tool-use, /docs/rate-limits, /docs/models
gerado_com: qwen/qwen3.6-27b + revisão humana
---

# Groq Free-tier: tool calling local (function calling)

Objetivo: o modelo pede ferramentas; **seu código** executa e devolve o resultado. Docs: [tool-use](https://console.groq.com/docs/tool-use).

## Ciclo

1. Envie `tools` (JSON Schema) + `messages`
2. Se vier `tool_calls`, execute a função local
3. Append `{ "role": "tool", "tool_call_id": "<id>", "name": "...", "content": "..." }`
4. Reenvie até a resposta final (sem novos `tool_calls`)

## Modelos Free (chat)

| ID | Parallel tools | Notas |
|----|----------------|-------|
| `qwen/qwen3.6-27b` | sim | recomendado no Free |
| `qwen/qwen3.8-27b` | não | |
| `openai/gpt-oss-20b` | não | built-in tools server-side também |
| `openai/gpt-oss-120b` | não | |

Confirme IDs em [models](https://console.groq.com/docs/models) e cotas Free em [rate-limits](https://console.groq.com/docs/rate-limits) (chat típico **30 RPM / 1K RPD / 8K TPM / 200K TPD**).

## JSON mínimo

```json
{
  "model": "qwen/qwen3.6-27b",
  "messages": [{"role": "user", "content": "Quanto é 21*2? Use a ferramenta."}],
  "tools": [{
    "type": "function",
    "function": {
      "name": "multiply",
      "description": "Multiplica dois inteiros",
      "parameters": {
        "type": "object",
        "properties": {
          "a": {"type": "integer"},
          "b": {"type": "integer"}
        },
        "required": ["a", "b"]
      }
    }
  }],
  "tool_choice": "auto",
  "max_tokens": 256
}
```

Key só via `GROQ_API_KEY`. Script: `tool_chat.py`.

## CTA

https://ziuluiziul.github.io/groq-round1-offer/ — kit **R$20** PIX Luiz.
