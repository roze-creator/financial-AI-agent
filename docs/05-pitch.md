# Pitch (3 minutos)

> [!TIP]
> Você pode usar alguns slides pra apoiar no seu Pitch e mostrar sua solução na prática.

## Roteiro Sugerido

### 1. O Problema (30 seg)
> Qual dor do cliente você resolve?

Você já olhou para o seu extrato bancário e não entendeu para onde foi o seu dinheiro? Brasileiros da classe média têm acesso a bancos digitais incríveis — mas nenhum deles te fala proativamente: *"Ei, você gastou 25% mais em alimentação esse mês. Vai impactar sua meta de comprar apartamento."*

A consultoria financeira personalizada é cara. Os bancos só falam com você quando você pergunta. E quando você pergunta, as respostas são genéricas. Isso é o problema que a **Burry** resolve.

---

### 2. A Solução (1 min)
> Como seu agente resolve esse problema?

A **Burry** é uma assistente financeira com IA Generativa que conhece **você de verdade**: seu perfil de investidor, suas metas, suas transações e seu histórico de atendimento.

Ela não espera você perguntar. Ela antecipa:
- Quando você pergunta sobre gastos, ela já te diz o impacto nas suas metas
- Quando você quer investir, ela considera seu perfil antes de sugerir qualquer produto
- Quando ela não sabe algo, ela diz — porque inventar informação financeira pode custar caro

Tecnicamente, a Burry usa o **Google Gemini** como cérebro, dados do cliente carregados via CSV e JSON, uma interface simples em **Streamlit** e um system prompt cuidadosamente construído com técnicas de few-shot prompting e anti-alucinação.

---

### 3. Demonstração (1 min)
> Mostre o agente funcionando (pode ser gravação de tela)

Na demonstração ao vivo (ou na gravação de tela), serão apresentados os seguintes cenários:

1. **Abertura:** João abre o app e a Burry já exibe um painel com o resumo financeiro do mês
2. **Consulta de gastos:** João pergunta "Quanto gastei com alimentação?" e recebe a resposta com os valores reais do CSV + contexto de impacto nas metas
3. **Recomendação de investimento:** João pergunta onde investir R$ 1.000 e a Burry sugere Tesouro Selic, explicando que Fundo de Ações não é ideal para o perfil dele
4. **Edge case:** João pergunta algo fora do escopo (previsão do tempo) e a Burry redireciona com simpatia

---

### 4. Diferencial e Impacto (30 seg)
> Por que essa solução é inovadora e qual é o impacto dela na sociedade?

O diferencial da Burry está em três pilares:

 **Proatividade:** Ela pensa com você, não só por você.

**Confiabilidade:** Sistema de anti-alucinação com regras rígidas — ela nunca inventa dado financeiro.

**Acessibilidade:** Qualquer pessoa com um smartphone pode ter uma consultora financeira pessoal, sem pagar nada.

O impacto é democratizar o planejamento financeiro no Brasil. 73% dos brasileiros não têm reserva de emergência. A Burry pode mudar esse número — uma conversa de cada vez.

---

## Checklist do Pitch

- [x] Duração máxima de 3 minutos
- [x] Problema claramente definido
- [x] Solução demonstrada na prática
- [x] Diferencial explicado
- [ ] Áudio e vídeo com boa qualidade

---

## Link do Vídeo

> Cole aqui o link do seu pitch (YouTube, Loom, Google Drive, etc.)

[Link do vídeo — a ser gravado após a implementação]
