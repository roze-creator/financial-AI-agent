# 🎬 Vídeo 1: Introdução ao Desafio

```
Fala, pessoal! Eu sou o Venilton, Tech Lead no time de Educação da DIO, e hoje vou apresentar pra vocês um desafio muito especial: criar um Agente Financeiro Inteligente usando IA Generativa.

Antes de entrar nos detalhes, deixa eu contextualizar.
Os assistentes virtuais no setor financeiro estão mudando. Eles estão deixando de ser aqueles chatbots básicos que só respondem perguntas prontas e estão se tornando agentes inteligentes e proativos.
Um bom exemplo disso é a Burry, a Inteligência Artificial do Bradesco, que evoluiu de um assistente reativo para um agente cada vez mais consultivo.
E é exatamente esse tipo de evolução que você vai explorar neste desafio.

Você vai criar um agente que não apenas responde, mas que antecipa necessidades. Que personaliza sugestões com base no perfil de cada cliente. Que ajuda a tomar decisões financeiras de forma consultiva. E, muito importante: que evita alucinações — ou seja, não inventa informações.

O que você vai entregar?
São seis etapas principais:
Primeiro: a documentação do agente — onde você define o caso de uso, a persona, a arquitetura e as estratégias de segurança.
Segundo: a base de conhecimento — usando os dados mockados que disponibilizamos ou datasets públicos que você preferir.
Terceiro: os prompts do agente — o coração do comportamento da sua solução.
Quarto: uma aplicação funcional — um protótipo que realmente funcione.
Quinto: avaliação e métricas — como você vai medir se o agente está funcionando bem.
E sexto: um pitch de três minutos — apresentando sua solução de forma objetiva.

Nos próximos vídeos, vou detalhar cada uma dessas etapas. E o mais importante: vamos colocar a mão na massa juntos! Cada vídeo terá uma parte prática onde eu mostro como fazer, deixando tudo documentado na pasta "examples" do repositório.

Mas quero deixar uma coisa bem clara: os exemplos são referências, não receitas prontas.
Independente de você estar em transição de carreira ou já ser especialista em tecnologia, o mais importante é dar a SUA cara ao desafio.
Use sua criatividade, explore suas ideias, e se permita ter essa experiência.

Bora começar?
```

---

# 🎬 Vídeo 2: Etapa 1 — Documentação do Agente

```
E aí, pessoal! Vamos pra primeira etapa do desafio: a Documentação do Agente.

Essa etapa é onde você define O QUE seu agente faz e COMO ele funciona. Parece simples, mas é aqui que muita gente pula e depois se perde no desenvolvimento.
Documentar bem no início economiza tempo depois.

Você vai preencher quatro seções principais no template.
A primeira é o Caso de Uso. Aqui você responde: qual problema financeiro meu agente resolve?
Pode ser consultoria de investimentos, planejamento de metas, alertas de gastos, ou qualquer outro cenário que faça sentido pra você.
O importante é ser específico. Não tente resolver tudo — foque em um problema bem definido.

A segunda seção é Persona e Tom de Voz.
Atenção: aqui estamos falando da personalidade do AGENTE, não do cliente.
Como o agente se comporta? Ele é mais formal ou informal? É consultivo, educativo, direto ao ponto?
Defina também exemplos de linguagem: como ele cumprimenta, como confirma informações, como responde quando não sabe algo.
Isso dá consistência pra experiência do usuário.

A terceira seção é a Arquitetura.
Você não precisa fazer nada super complexo aqui. Um diagrama simples mostrando o fluxo: usuário faz pergunta, agente processa, consulta a base de conhecimento, valida a resposta e devolve pro usuário.
No template tem um exemplo em Mermaid que você pode adaptar.

E a quarta seção é Segurança e Anti-Alucinação.
No setor financeiro, isso é crítico. Seu agente não pode inventar informações.
Então defina estratégias: ele só responde com base nos dados fornecidos? Ele cita a fonte da informação? Quando não sabe, ele admite?
Liste também as limitações — o que o agente NÃO faz.

Lembre-se: o template é um guia, não uma camisa de força. Adapte conforme a sua ideia e o seu caso de uso.

Agora vamos pra parte prática! Vou mostrar como eu preencheria essa documentação passo a passo. Tudo vai ficar registrado na pasta "examples" pra você consultar depois.
Bora lá!
```

---

# 🎬 Vídeo 3: Etapa 2 — Base de Conhecimento

```
Fala, pessoal! Agora vamos falar sobre a Base de Conhecimento do seu agente.

Todo agente inteligente precisa de dados pra trabalhar. No nosso caso, disponibilizamos quatro arquivos mockados na pasta "data" do repositório.
São dados simples, seguros e sem informações sensíveis — perfeitos pra você focar no desenvolvimento sem se preocupar com privacidade.

Deixa eu explicar cada arquivo.
O primeiro é o "transacoes.csv" — um histórico de transações do cliente em formato CSV. Tem data, descrição, categoria, valor e se é entrada ou saída.
O segundo é o "historico_atendimento.csv" — também em CSV, com registros de atendimentos anteriores. Útil pra dar contexto pro agente sobre interações passadas.
O terceiro é o "perfil_investidor.json" — contém informações do cliente como nome, idade, renda, perfil de investidor e metas financeiras.
E o quarto é o "produtos_financeiros.json" — uma lista de produtos disponíveis como Tesouro Selic, CDB, LCI, fundos... cada um com categoria, risco, rentabilidade e pra quem é indicado.

A ideia é que você use esses dados como base de conhecimento do agente. Pode carregar no início da sessão e incluir no contexto do prompt, ou consultar dinamicamente dependendo da pergunta do usuário.

Você pode — e deve — adaptar esses dados pro seu caso de uso. Se quiser adicionar mais transações, criar novos produtos, modificar o perfil... fique à vontade!
E se preferir usar um dataset mais robusto, o Hugging Face tem vários datasets públicos relacionados a finanças.
O importante é que os dados façam sentido pro problema que você escolheu resolver.

No template da documentação, descreva quais arquivos você usou e como. Explique sua estratégia de integração e mostre um exemplo de contexto formatado.

Agora vamos pro hands-on! Vou mostrar na prática como organizar e integrar esses dados. Fica tudo na pasta "examples" pra você usar como referência.
Vamos lá!
```

---

# 🎬 Vídeo 4: Etapa 3 — Prompts do Agente

```
E aí, pessoal! Chegamos numa das etapas mais importantes: os Prompts do Agente.

Se eu tivesse que dar uma única dica pra esse desafio, seria: comece pelo prompt. Um bom system prompt é a base de um agente eficaz.
É no prompt que você define as regras do jogo. Como o agente se comporta, o que ele pode e não pode fazer, como ele deve responder em diferentes situações.

No template, você vai documentar três coisas principais.
A primeira é o System Prompt — as instruções gerais do agente.
Aqui você define quem ele é, qual o objetivo dele, e as regras que ele deve seguir.
Por exemplo: "Você é um agente financeiro especializado em investimentos. Seu objetivo é ajudar o cliente a tomar decisões informadas. Regra um: sempre baseie suas respostas nos dados fornecidos. Regra dois: nunca invente informações financeiras. Regra três: se não souber algo, admita e ofereça alternativas."

A segunda parte são os Exemplos de Interação.
Crie cenários de uso mostrando entrada e saída esperada. Isso ajuda tanto você a validar o comportamento, quanto quem for avaliar seu projeto a entender como funciona.
Uma técnica muito útil aqui é o Few-Shot Prompting: dar exemplos de perguntas e respostas ideais dentro do próprio prompt. Quanto mais claro você for nas instruções, menos o agente vai alucinar.

A terceira parte é o Tratamento de Edge Cases — as situações limite.
O que acontece quando o usuário pergunta algo fora do escopo? E se tentarem obter informação sensível? E se pedirem recomendação sem contexto suficiente?
Documente como o agente deve se comportar em cada caso.

Uma dica importante: itere nos prompts.
Seu primeiro prompt provavelmente não vai ser perfeito. Teste, veja onde falha, ajuste, teste de novo.
No template tem um espaço pra registrar observações e aprendizados. Documenta o que você mudou e por quê.

Mas lembre-se: o exemplo que eu vou mostrar é uma referência. Seu prompt deve refletir o SEU caso de uso e a personalidade do SEU agente.

Agora vamos pro hands-on! Vou construir um system prompt do zero e mostrar o processo de refinamento. Tudo documentado na pasta "examples".
Bora!
```

---

# 🎬 Vídeo 5: Etapa 4 — Aplicação Funcional

```
Fala, pessoal! Agora vamos falar da parte prática: a Aplicação Funcional.

Até agora você definiu o que o agente faz, organizou os dados e criou os prompts. Agora é hora de colocar tudo isso pra funcionar.
O objetivo aqui é criar um protótipo funcional — não precisa ser perfeito, mas precisa funcionar.

O que você precisa entregar?
Um chatbot interativo onde o usuário consegue conversar com o agente. Integração com um LLM — pode ser via API ou modelo local. E conexão com a base de conhecimento que você preparou.

Que ferramentas usar?
Pra interface, sugerimos Streamlit ou Gradio. São simples, rápidas de implementar e têm versões gratuitas. Se você já domina outra ferramenta, pode usar também.
Pro LLM, você pode usar ChatGPT, Claude, Gemini via API... ou rodar um modelo local com Ollama se preferir.
Se quiser orquestrar fluxos mais complexos, ferramentas como LangChain, LangFlow ou CrewAI podem ajudar.

Na pasta "src" do repositório, tem um README com a estrutura sugerida.
Basicamente: um arquivo principal da aplicação, um arquivo com a lógica do agente, um arquivo de configuração pras suas API keys, e um requirements.txt com as dependências.

Algumas dicas práticas:
Comece simples. Faça funcionar primeiro, depois melhora.
Teste com as perguntas dos cenários que você definiu nos prompts. Veja se o agente responde como esperado.
Se algo não funcionar, volte pro prompt e ajuste. Muitas vezes o problema não é no código, é na instrução.

E lembre-se: não existe uma única forma certa de fazer isso. Use as ferramentas que você conhece ou aproveite pra aprender algo novo. O importante é entregar algo funcional que resolva o problema que você definiu.

Agora vamos pro hands-on! Vou criar uma aplicação simples em Streamlit conectada ao agente. O código completo vai estar na pasta "examples" pra você adaptar.
Vamos lá!
```

---

# 🎬 Vídeo 6: Etapa 5 — Avaliação e Métricas

```
E aí, pessoal! Vamos falar sobre como avaliar seu agente.

Criar o agente é uma parte. Saber se ele está funcionando bem é outra igualmente importante.
A avaliação pode ser feita de duas formas complementares: testes estruturados, onde você define perguntas e respostas esperadas, e feedback real, onde outras pessoas testam e dão notas.

No template, sugerimos três métricas principais.
A primeira é Assertividade: o agente respondeu o que foi perguntado? Se você pergunta o saldo, ele tem que retornar o valor correto.
A segunda é Segurança: o agente evitou inventar informações? Se você pergunta algo que não está nos dados, ele deve admitir que não sabe.
A terceira é Coerência: a resposta faz sentido pro perfil do cliente? Se o cliente é conservador, o agente não deve sugerir investimento de alto risco.

Crie casos de teste simples pra validar cada métrica.
No template tem quatro exemplos: consulta de gastos, recomendação de produto, pergunta fora do escopo e informação inexistente.
Rode esses testes, marque se passou ou não, e registre o que funcionou e o que pode melhorar.

Uma dica muito boa: peça pra três a cinco pessoas testarem seu agente. Pode ser amigo, familiar, colega de trabalho.
Peça pra eles avaliarem cada métrica com notas de um a cinco. Isso torna sua avaliação muito mais confiável.
Se você usou os dados da pasta "data", lembre de contextualizar os participantes sobre o cliente fictício representado ali.

Pra quem quer ir além, tem uma seção opcional de métricas avançadas. Coisas como latência, consumo de tokens, taxa de erros... Ferramentas como LangWatch e LangFuse podem ajudar.
Mas isso é opcional — foque primeiro nas métricas básicas.

Agora vamos pro hands-on! Vou mostrar como estruturar e executar esses testes na prática. Tudo vai estar documentado na pasta "examples".
Vamos lá!
```

---

# 🎬 Vídeo 7: Etapa 6 — Pitch

```
Fala, pessoal! Última etapa de entrega: o Pitch.

Você vai gravar um vídeo de no máximo três minutos apresentando sua solução de forma objetiva.
Três minutos passam muito rápido, então vá direto ao ponto.

O template sugere um roteiro em quatro partes.
Nos primeiros trinta segundos, apresente o problema. Qual dor do cliente você resolve? Seja específico e conecte com uma situação real.
No próximo um minuto, explique a solução. Como seu agente resolve esse problema? Quais são as principais funcionalidades?
Depois, use um minuto pra demonstração. Mostre o agente funcionando na prática. Pode ser uma gravação de tela — não precisa ser ao vivo.
E nos últimos trinta segundos, fale do diferencial. Por que sua solução é inovadora? Qual o impacto dela?

Algumas dicas práticas:
Ensaie antes de gravar. Três minutos é pouco tempo pra improvisar.
Cuide da qualidade do áudio e do vídeo. Não precisa ser profissional, mas precisa ser compreensível.
Use slides de apoio se ajudar, mas não dependa deles. O foco é você explicando e mostrando o agente.

No template tem um checklist pra você validar antes de enviar.
E lembre-se: o pitch é a SUA apresentação. Mostre sua personalidade, conte sua história com o projeto. Isso faz diferença!

Agora vamos pro hands-on! Vou mostrar como estruturar um pitch e dar dicas de gravação. O exemplo completo fica na pasta "examples".
Vamos finalizar!
```

---

# 🎬 Vídeo 8: Dicas Finais

```
E aí, pessoal! Pra fechar, quero deixar algumas dicas finais que vão te ajudar a entregar um projeto de qualidade.

Dica número um: comece pelo prompt.
Eu sei que já falei isso algumas vezes, mas vale repetir. Um bom system prompt é a base de tudo. Se o prompt estiver bem feito, o resto flui.

Dica número dois: use os dados mockados.
Eles estão lá pra facilitar sua vida. São simples, seguros e consistentes. Você pode adaptar e expandir, mas não precisa criar do zero.

Dica número três: foque na segurança.
No setor financeiro, alucinação é inaceitável. Seu agente não pode inventar taxa de rendimento, não pode sugerir produto que não existe, não pode dar informação errada.
Defina regras claras no prompt e teste os edge cases.

Dica número quatro: teste com cenários reais.
Não teste só o caminho feliz. Simule perguntas que um cliente de verdade faria. Tente quebrar o agente. Veja onde ele falha.
É melhor você descobrir os problemas do que o avaliador.

Dica número cinco: seja direto no pitch.
Três minutos é muito pouco tempo. Não enrole na introdução. Vá direto ao problema, mostre a solução, demonstre funcionando.

Dica número seis: pense em quem vai usar.
Tecnologia boa é tecnologia que serve a todos. Quando você criar seu agente, pense em acessibilidade, em linguagem inclusiva, em como diferentes pessoas vão interagir com ele. Empatia no design faz toda a diferença.

E a dica mais importante de todas: dê a SUA cara ao desafio.
Os exemplos que mostrei nos vídeos são referências, não respostas prontas. Não importa se você está começando agora ou já tem anos de experiência — o mais valioso é você se permitir explorar, errar, aprender e criar.
Sua solução não precisa ser igual a de ninguém. Ela precisa ser sua.

Na pasta "examples" do repositório você encontra tudo que fizemos juntos. Use como ponto de partida e evolua a partir dali.

É isso, pessoal!
Agora é com vocês. Mãos à obra e bora criar esse agente!
Qualquer dúvida, nos vemos no fórum.
Valeu e bons estudos!

```

