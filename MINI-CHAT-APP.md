---
produto: Mini chat app Groq Free
preco_sugerido_BRL: 20
http: 200
rpd_rem: 998
tpm_rem: 6919
---

# Mini Chat App com Groq (Qwen 3.6-27B)

Este guia mostra como criar um chat simples usando Groq via `curl` e HTML mínimo, sem necessidade de API keys.

## Pré-requisitos

- Navegador moderno
- Terminal com `curl`
- Conexão à internet

## Estrutura do Projeto

```
chat-app/
├── index.html
└── chat.sh
```

## Passo 1: Criar o Script de Backend (chat.sh)

```bash
#!/bin/bash

# Recebe a mensagem do usuário
MESSAGE=$1

# Faz a requisição para Groq
RESPONSE=$(curl -s -X POST "https://api.groq.com/openai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "User-Agent: groq-python/1.0" \
  -d "{
    \"model\": \"qwen/qwen3.6-27b\",
    \"messages\": [{\"role\": \"user\", \"content\": \"$MESSAGE\"}],
    \"max_tokens\": 1024
  }")

# Verifica se houve erro 429 (Too Many Requests)
if echo "$RESPONSE" | grep -q "429"; then
  RETRY_AFTER=$(echo "$RESPONSE" | grep -o '"Retry-After": [0-9]*' | cut -d' ' -f2)
  echo "Aguarde $RETRY_AFTER segundos antes de tentar novamente."
  exit 1
fi

# Extrai a resposta do modelo
echo "$RESPONSE" | grep -o '"content": "[^"]*"' | cut -d'"' -f4
```

## Passo 2: Criar o Frontend (index.html)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Mini Chat com Groq</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; }
    #chat { border: 1px solid #ccc; height: 300px