---
round: 1
gerado: 2026-09-05 14:19 UTC
modelo: qwen/qwen3.6-27b
http: 200
rpd_remaining: 999
tpm_remaining: 7624
usage: prompt=308 completion=1600 total=1908
preco_BRL: 20
pix: /workspace/pix-clean/out/pix_copia_cola_1.txt + qr_1.png
usd: pending Binance (Luiz — não inventar wallet)
---

# Relatório ROUND1 — Smoke + limites GroqCloud Free-tier (2026-09-05)

## 1. Resumo Executivo

Este documento consolida os resultados do teste de fumaça (smoke test) realizado na infraestrutura GroqCloud, focando especificamente nas restrições do plano gratuito (Free-tier). A análise valida a integridade das conexões HTTP/1.1 e a aderência aos limites de taxa (rate limits) para os modelos selecionados. Identificou-se que o plano Free opera com cotas rígidas de requisições por minuto (RPM) e tokens por dia (TPD), distintas das colunas "Developer" (PAYG) documentadas. O relatório estabelece a base técnica para validação pré-venda, garantindo que a integração respeite os limites organizacionais e evite bloqueios por erro 429, além de detalhar a estrutura de cobrança via PIX para fins de reembolso interno.

## 2. IDs Chat Free Típicos e Limites Oficiais

Os limites abaixo aplicam-se estritamente ao **Free Plan**. É crucial distinguir estas cotas das colunas "Developer" ou "Pro" encontradas na documentação pública, que operam sob modelo *Pay-As-You-Go* (PAYG).

| Modelo (ID) | RPM (Reqs/Min) | RPD (Reqs/Dia) | TPM (Tokens/Min) | TPD (Tokens/Dia) |
| :--- | :---: | :---: | :---: | :---: |
| `openai/gpt-oss-20b` | 30 | 1.000 | 8.000 | 200.000 |
| `openai/gpt-oss-120b` | 30 | 1.000 | 8.000 | 200.000 |
| `qwen/qwen3.6-27b` | 30 | 1.000 | 8.000 | 200.000 |
| `qwen/qwen3.8-27b` | 30 | 1.000 | 8.000 | 200.000 |

**Nota Técnica:** Os limites são aplicados por chave de API (`GROQ_API_KEY`) e não por endpoint individual. O excedente resulta em recusa imediata da requisição.

## 3. Procedimento de Smoke HTTP/1.1

O teste de fumaça valida a conectividade básica e a resposta do servidor a condições de saturação.

**Configuração da Requisição:**
*   **Protocolo:** HTTP/1.1
*   **Host:** `api.groq.com`
*   **Path:** `/openai/v1/chat/completions`
*   **User-Agent:** `groq-python/1.0`
*   **Autenticação:** Cabeçalho `Authorization: Bearer <GROQ_API_KEY>`

**Fluxo de Validação:**
1.  **Envio de Payload Mínimo:** Submissão de uma requisição JSON válida com `model` definido e `messages` contendo um único turno de usuário.
2.  **Verificação de Sucesso (200 OK):** Confirmação de que o corpo da resposta contém o campo `choices` com `message.content` não nulo.
3.  **Simulação de Limite (429 Too Many Requests):** Execução rápida de requisições excedendo o RPM de 30.
4.  **Análise de Retry-After:** Inspeção do cabeçalho de resposta `Retry-After` para validar o tempo de espera sugerido pelo servidor antes da próxima tentativa.
5.  **Verificação Org-Level:** Confirmação de que os limites são aplicados no nível da organização associada à chave, impedindo contornar restrições via múltiplas chaves no mesmo escopo Free.

## 4. Checklist Pré-Venda

Antes da implementação em produção ou demonstração comercial, os seguintes itens devem ser verificados para evitar falhas críticas e violações de contrato de serviço.

*   [ ] **Segurança de Secrets:** Garantir que a `GROQ_API_KEY` não está hardcoded no código-fonte. Utilizar variáveis de ambiente (`env GROQ_API_KEY`) ou gerenciadores de segredos (ex: AWS Secrets Manager, HashiCorp Vault).
*   [ ] **Distinção de Planos:** Confirmar que a documentação interna não confunde os limites do "Free Tier" com a coluna "Developer" (PAYG) do site `/docs/models`. O Free Tier tem cotas diárias fixas; o Developer escala conforme o uso pago.
*   [ ] **Tratamento de Erros 429:** Implementar lógica de *exponential backoff* no cliente Python/Node.js para respeitar o cabeçalho `Retry-After` e evitar loops infinitos de requisição.
*   [ ] **Validação de Modelo:** Assegurar que os IDs dos modelos (`openai/gpt-oss-20b`, etc.) estão corretamente mapeados na configuração do aplicativo, pois IDs incorretos retornam 404 ou 400, não 429.
*   [ ] **Monitoramento de TPD:** Implementar alertas quando o consumo de tokens se aproximar do limite de 200.000 TPD para evitar interrupções no final do dia útil.

## 5. Anexo: PIX Luiz (paths oficiais)

| Valor | Copia-e-cola | QR |
|------|--------------|-----|
| R$ 10 | `pix_copia_cola_0.txt` | `qr_0.png` |
| R$ 20 | `pix-r20.txt` / `pix_copia_cola_1.txt` | `qr-r20.png` |
| R$ 50 | `pix-r50.txt` / `pix_copia_cola_2.txt` | `qr-r50.png` |
| R$ 100 | `pix_copia_cola_3.txt` | `qr_3.png` |
| R$ 200 | `pix_copia_cola_4.txt` | `qr_4.png` |
| Livre | `pix_copia_cola_5.txt` | `qr_5.png` |

Payloads embutidos na landing Pages e nos ficheiros deste repo (override Luiz). USD→Binance (Luiz).
