---
produto: Watchdog cotas Groq Free
preco_sugerido_BRL: 20
pix: pix-r20.txt / qr-r20.png
modelo: qwen/qwen3.8-27b
http: 200
rpd_rem: 999
tpm_rem: 7346
region: msp
usage: {"queue_time": 0.092463613, "prompt_tokens": 298, "prompt_time": 0.023727504, "completion_tokens": 650, "completion_time": 1.279636396, "total_tokens": 948, "total_time": 1.3033639}
companion: rate_limit_watchdog.py
---

# Watchdog de Cotas Groq Free (RPD/TPM)

Gerenciar a taxa de requisições (rate limiting) na camada de organização é crítico para evitar interrupções abruptas em produção. Este guia apresenta uma estratégia robusta para monitorar e regular o consumo de API na Groq, focando na sustentabilidade do plano gratuito.

## 1. Por que monitorar ativamente?

Os limites de taxa na Groq são aplicados no nível da organização (*org-level*), não por chave individual. Ignorar esses limites resulta em respostas HTTP `429 Too Many Requests`, que podem derrubar fluxos de trabalho inteiros.

A chave para o controle proativo reside nos cabeçalhos de resposta da API:
*   **`x-ratelimit-remaining-requests`**: Indica as requisições diárias restantes (RPD).
*   **`x-ratelimit-remaining-tokens`**: Indica os tokens por minuto restantes (TPM).

Monitorar esses valores permite antecipar o esgotamento da cota antes que o erro ocorra.

## 2. A Regra de Ouro

Para garantir a estabilidade do serviço, implemente uma lógica de parada preventiva:
1.  **Parar imediatamente** se o uso de RPD atingir **80%** do limite diário.
2.  **Parar imediatamente** se o saldo residual de TPM for inferior a **400 tokens**.
3.  **Respeitar rigorosamente** o cabeçalho `Retry-After` quando um erro 429 for retornado. Tentativas de "força bruta" apenas prolongam a penalização.

## 3. Fórmula de Pacing 24/7

O plano gratuito de chat da Groq tipicamente oferece **30 RPM** (Requisições por Minuto), **1.000 RPD** (Requisições por Dia) e **8.000 TPM** (Tokens por Minuto).

Para operar 24/7 sem estourar a cota diária, a distribuição deve ser uniforme. Se você espalhar as 1.000 requisições diárias ao longo de 24 horas, o teto máximo sustentável é de aproximadamente **40 requisições por hora**.

> **Atenção:** Nunca tente "burstar" (enviar em rajada) as 30 RPM permitidas sem margem de segurança. O consumo de tokens (TPM) é o gargalo mais comum. Mantenha uma média baixa de requisições para garantir que o TPM não zere antes do RPD.

## 4. Implementação: Script Companion

Para automatizar essa lógica, utilize o script `rate_limit_watchdog.py`. Este utilitário:
1.  Realiza um *ping* leve à API.
2.  Lê os cabeçalhos `x-ratelimit-remaining-requests` e `x-ratelimit-remaining-tokens`.
3.  Avalia as regras de parada definidas acima.
4. 