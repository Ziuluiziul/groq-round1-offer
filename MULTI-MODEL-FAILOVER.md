---
produto: Failover multi-modelo Groq Free
preco_sugerido_BRL: 20
pix: pix-r20.txt / qr-r20.png
modelo: qwen/qwen3.6-27b
http: 200
rpd_rem: 998
tpm_rem: 7082
region: msp
usage: {"queue_time": 0.004189763, "prompt_tokens": 268, "prompt_time": 0.019670128, "completion_tokens": 650, "completion_time": 1.293782088, "total_tokens": 918, "total_time": 1.313452216}
companion: multi_model_chat.py
---

# Failover multi-modelo Groq Free-tier

A API gratuita da Groq oferece latência impressionante, mas impõe limites rigorosos de taxa (Rate Limits) que podem interromper aplicações críticas se não forem gerenciados corretamente. Este guia apresenta uma estratégia de failover robusta para maximizar a disponibilidade no plano Free, evitando erros `429 Too Many Requests` e garantindo continuidade de serviço.

## 1. Por que implementar Failover?

No plano Free, os limites são definidos por **RPD** (Requisições por Dia) e **TPM** (Tokens por Minuto) por modelo. Além disso, a Groq aplica limites organizacionais (`org-level`). Se um modelo específico esgota sua cota diária ou atinge o limite de tokens, a API retorna um erro `429`.

Sem uma estratégia de failover, sua aplicação falha silenciosamente ou retorna erros ao usuário. Com failover, o sistema redireciona automaticamente a solicitação para outro modelo disponível, mantendo a experiência do usuário ininterrupta.

## 2. Ordem Sugerida de Chat (Free Tier)

Utilize apenas IDs oficiais ativos. A ordem abaixo prioriza modelos com melhor custo-benefício em latência e disponibilidade atual:

1.  `qwen/qwen3.6-27b`
2.  `openai/gpt-oss-20b`
3.  `qwen/qwen3.8-27b`
4.  `openai/gpt-oss-120b`

> **Nota:** Esta ordem pode ser ajustada conforme a disponibilidade real em tempo real, mas deve ser mantida como padrão inicial.

## 3. Regras de Ouro para Implementação

Para garantir conformidade e evitar bloqueios temporários da sua conta, siga estas regras estritamente:

*   **Uma tentativa por modelo:** Em caso de erro `429`, tente o modelo seguinte na lista. Não repita a tentativa no mesmo modelo imediatamente.
*   **Respeite o `Retry-After`:** Se o cabeçalho HTTP retornar `Retry-After`, aguarde o tempo especificado antes de qualquer nova tentativa, mesmo em outro modelo.
*   **Monitoramento de RPD:** Verifique o cabeçalho `remaining-requests`. Se o uso diário atingir **80%** da cota total, pare de enviar requisições para esse modelo específico até a próxima rotação diária (UTC).
*   **Segurança:** Nunca *hardcode* sua chave de API (`GROQ_API_KEY`). Utilize variáveis de ambiente ou gerenciadores de segredos.

## 4. Pseudo-fluxo de Execução

O script companheiro `multi_model_chat.py` implementa a seguinte lógica:

```python
def chat_with_failover(prompt):
    models = [
        "qwen/qwen3.6-27b",
        "openai/gpt-oss-20b",
        "qwen/q