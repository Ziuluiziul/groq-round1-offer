---
produto: JSON mode Groq Free
preco_BRL: 10
fontes: console.groq.com/docs/rate-limits, /models, /deprecations
---

# Groq Free-tier: JSON mode (`response_format`) na prática

Objetivo: respostas **parseáveis** sem gastar cota à toa.

## Chamada

```json
{
  "model": "openai/gpt-oss-20b",
  "messages": [
    {"role": "system", "content": "Responda só JSON válido."},
    {"role": "user", "content": "Schema: {\"ok\": bool, \"msg\": string}"}
  ],
  "response_format": {"type": "json_object"},
  "max_tokens": 256
}
```

- `response_format.type = json_object` pede JSON.
- Ainda assim: **valide no cliente** (`json.loads`) e, se quiser, schema (pydantic/jsonschema).
- Key só em `GROQ_API_KEY`. Header `User-Agent: groq-python/1.0`.

## Modelos chat Free (IDs — limites na tabela Free)

Confirme disponibilidade em [models](https://console.groq.com/docs/models) e cotas em [rate-limits](https://console.groq.com/docs/rate-limits):

- `qwen/qwen3.6-27b` / `qwen/qwen3.8-27b`
- `openai/gpt-oss-20b` / `openai/gpt-oss-120b`

Llama 3.1/3.3 podem sumir do free — veja [deprecations](https://console.groq.com/docs/deprecations).

## Falhas comuns

| Sintoma | Mitigação |
|---------|-----------|
| Fence ` ```json ` | strip antes do `loads` |
| Texto “thinking” / preâmbulo | prompt “só JSON” + `response_format` + modelo que não vaze raciocínio |
| `json_validate_failed` (400) | simplificar schema / reduzir output |
| 429 tokens (TPM/OTPM) | `max_tokens` menor + esperar `retry-after` / reset |

Script: `json_chat.py`.

## CTA

https://ziuluiziul.github.io/groq-round1-offer/ — tip **R$10** / kit **R$20** (PIX Luiz).
