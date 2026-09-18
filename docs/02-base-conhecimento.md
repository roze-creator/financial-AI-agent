# Base de Conhecimento

## Dados Utilizados

Todos os arquivos mockados da pasta `data/` foram utilizados, sem modificações externas:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores do cliente para dar continuidade ao atendimento |
| `perfil_investidor.json` | JSON | Personalizar recomendações com base no perfil, renda, metas e tolerância a risco |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil e situação financeira do cliente |
| `transacoes.csv` | CSV | Analisar padrão de gastos por categoria e alertar sobre desvios |

---

## Adaptações nos Dados

Os dados mockados foram utilizados **sem alteração**, pois já representam adequadamente o perfil do cliente fictício (João Silva). O agente é construído de forma que **qualquer futuro usuário possa ter seus próprios dados carregados** em substituição aos arquivos mockados.

Para uma versão de produção, bastaria conectar os arquivos CSV/JSON a uma API bancária real que exporte dados no mesmo formato.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os quatro arquivos são carregados na inicialização do app (`app.py`) usando `pandas` (para CSV) e `json` (para JSON). Todos os dados são transformados em texto estruturado e injetados no **system prompt** uma única vez por sessão. Não há banco de dados ou embedding vetorial, a abordagem é simples e funcional para o escopo do desafio.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados são incluídos diretamente no **system prompt** que inicializa a sessão de chat. O Gemini recebe um prompt de sistema com:
1. A persona e as regras de comportamento da Burry
2. O perfil completo do cliente (JSON)
3. As últimas transações (CSV convertido para texto)
4. Os produtos financeiros disponíveis (JSON)
5. O histórico de atendimentos anteriores (CSV)

Essa abordagem garante que o LLM tenha todo o contexto necessário para qualquer pergunta do cliente sem precisar de buscas adicionais.

---

## Exemplo de Contexto Montado

```
=== DADOS DO CLIENTE ===
Nome: João Silva
Idade: 32 anos
Profissão: Analista de Sistemas
Renda Mensal: R$ 5.000,00
Perfil Investidor: Moderado
Aceita Risco: Não
Patrimônio Total: R$ 15.000,00
Reserva de Emergência Atual: R$ 10.000,00

=== METAS FINANCEIRAS ===
1. Completar reserva de emergência | Valor necessário: R$ 15.000,00 | Prazo: Junho/2026
2. Entrada do apartamento | Valor necessário: R$ 50.000,00 | Prazo: Dezembro/2027

=== ÚLTIMAS TRANSAÇÕES (Outubro/2025) ===
01/10 - Salário (receita): +R$ 5.000,00
02/10 - Aluguel (moradia): -R$ 1.200,00
03/10 - Supermercado (alimentação): -R$ 450,00
05/10 - Netflix (lazer): -R$ 55,90
07/10 - Farmácia (saúde): -R$ 89,00
10/10 - Restaurante (alimentação): -R$ 120,00
12/10 - Uber (transporte): -R$ 45,00
15/10 - Conta de Luz (moradia): -R$ 180,00
20/10 - Academia (saúde): -R$ 99,00
25/10 - Combustível (transporte): -R$ 250,00
Total de saídas: R$ 2.488,90 | Saldo estimado disponível: R$ 2.511,10

=== PRODUTOS FINANCEIROS DISPONÍVEIS ===
1. Tesouro Selic | Renda Fixa | Risco: Baixo | Rentabilidade: 100% Selic | Mínimo: R$ 30
2. CDB Liquidez Diária | Renda Fixa | Risco: Baixo | Rentabilidade: 102% CDI | Mínimo: R$ 100
3. LCI/LCA | Renda Fixa | Risco: Baixo | Rentabilidade: 95% CDI | Mínimo: R$ 1.000 (isento IR)
4. Fundo Multimercado | Fundo | Risco: Médio | Rentabilidade: CDI+2% | Mínimo: R$ 500
5. Fundo de Ações | Fundo | Risco: Alto | Rentabilidade: Variável | Mínimo: R$ 100

=== HISTÓRICO DE ATENDIMENTOS ===
15/09/2025 - Chat - CDB: Cliente perguntou sobre rentabilidade e prazos (resolvido)
22/09/2025 - Telefone - App: Erro ao visualizar extrato foi corrigido (resolvido)
01/10/2025 - Chat - Tesouro Selic: Cliente pediu explicação sobre funcionamento (resolvido)
12/10/2025 - Chat - Metas: Cliente acompanhou progresso da reserva de emergência (resolvido)
25/10/2025 - Email - Cadastro: Cliente atualizou e-mail e telefone (resolvido)
```
