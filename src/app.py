"""
Burry - Assistente Financeiro Inteligente
Desafio DIO: Agente Financeiro com IA Generativa

Recursos:
    - Chat consultivo com IA Generativa (Google Gemini)
    - Edição e inserção de dados mockados (Transações de Entrada e Saída)
    - Cálculo dinâmico em tempo real de saldo disponível
    - Persistência e restauração de dados

Requisitos:
    pip install streamlit google-generativeai pandas

Executar:
    python -m streamlit run src/app.py
"""

import os
import json
from datetime import date
import pandas as pd
import streamlit as st
import google.generativeai as genai

# ──────────────────────────────────────────────
# Configuração da página
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Burry – Assistente Financeiro",
    page_icon="💚",
    layout="wide",
)

# ──────────────────────────────────────────────
# Carregamento e salvamento dos dados
# ──────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CSV_TRANSACOES = os.path.join(DATA_DIR, "transacoes.csv")
JSON_PERFIL = os.path.join(DATA_DIR, "perfil_investidor.json")
JSON_PRODUTOS = os.path.join(DATA_DIR, "produtos_financeiros.json")
CSV_HISTORICO = os.path.join(DATA_DIR, "historico_atendimento.csv")


def carregar_perfil_disco():
    with open(JSON_PERFIL, encoding="utf-8") as f:
        return json.load(f)


def carregar_produtos():
    with open(JSON_PRODUTOS, encoding="utf-8") as f:
        return json.load(f)


def carregar_transacoes_disco():
    df = pd.read_csv(CSV_TRANSACOES)
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0.0)
    return df


def carregar_historico():
    return pd.read_csv(CSV_HISTORICO)


def salvar_transacoes_disco(df):
    df.to_csv(CSV_TRANSACOES, index=False)


def salvar_perfil_disco(perfil_dict):
    with open(JSON_PERFIL, "w", encoding="utf-8") as f:
        json.dump(perfil_dict, f, indent=2, ensure_ascii=False)


# ──────────────────────────────────────────────
# Montagem do contexto para o system prompt
# ──────────────────────────────────────────────
def montar_contexto(perfil, transacoes, produtos, historico, nome_usuario):
    """Transforma os dados atuais em texto estruturado para o LLM."""

    metas_texto = "\n".join(
        f"  - {m['meta']} | Valor: R$ {m['valor_necessario']:,.2f} | Prazo: {m['prazo']}"
        for m in perfil.get("metas", [])
    )

    perfil_texto = f"""
=== DADOS DO CLIENTE ===
Nome preferido: {nome_usuario}
Idade: {perfil.get('idade', 30)} anos
Profissão: {perfil.get('profissao', 'Profissional')}
Renda Mensal: R$ {perfil.get('renda_mensal', 0.0):,.2f}
Perfil Investidor: {str(perfil.get('perfil_investidor', 'moderado')).capitalize()}
Aceita Risco Alto: {'Sim' if perfil.get('aceita_risco', False) else 'Não'}
Patrimônio Total: R$ {perfil.get('patrimonio_total', 0.0):,.2f}
Reserva de Emergência Atual: R$ {perfil.get('reserva_emergencia_atual', 0.0):,.2f}
Objetivo Principal: {perfil.get('objetivo_principal', 'Segurança Financeira')}

=== METAS FINANCEIRAS ===
{metas_texto}
"""

    entradas = transacoes[transacoes["tipo"] == "entrada"]["valor"].sum()
    saidas = transacoes[transacoes["tipo"] == "saida"]["valor"].sum()
    saldo = entradas - saidas

    linhas_transacoes = "\n".join(
        f"  {row['data']} - {row['descricao']} ({row['categoria']}): "
        f"{'+ ' if row['tipo'] == 'entrada' else '- '}R$ {row['valor']:,.2f}"
        for _, row in transacoes.iterrows()
    )

    transacoes_texto = f"""
=== TRANSAÇÕES ATUAIS ===
{linhas_transacoes}

RESUMO FINANCEIRO CALCULADO:
- Total de Entradas: R$ {entradas:,.2f}
- Total de Saídas/Despesas: R$ {saidas:,.2f}
- Saldo Disponível: R$ {saldo:,.2f}
"""

    linhas_produtos = "\n".join(
        f"  - {p['nome']} | {p['categoria'].replace('_',' ').title()} | "
        f"Risco: {p['risco'].capitalize()} | Rentabilidade: {p['rentabilidade']} | "
        f"Mínimo: R$ {p['aporte_minimo']:,.2f} | {p['indicado_para']}"
        for p in produtos
    )

    produtos_texto = f"""
=== PRODUTOS FINANCEIROS DISPONÍVEIS ===
{linhas_produtos}
"""

    linhas_historico = "\n".join(
        f"  {row['data']} - {row['canal'].title()} - {row['tema']}: {row['resumo']} "
        f"({'✅ resolvido' if row['resolvido'] == 'sim' else '⏳ pendente'})"
        for _, row in historico.iterrows()
    )

    historico_texto = f"""
=== HISTÓRICO DE ATENDIMENTOS ANTERIORES ===
{linhas_historico}
"""

    return perfil_texto + transacoes_texto + produtos_texto + historico_texto


# ──────────────────────────────────────────────
# System prompt do Burry
# ──────────────────────────────────────────────
def criar_system_prompt(contexto, nome_usuario):
    return f"""Você é o Burry, um assistente financeiro virtual inteligente, empático e proativo.
Seu objetivo é ajudar o cliente a entender suas finanças, acompanhar suas metas e tomar decisões inteligentes com base em dados.
Chame o cliente sempre pelo nome: {nome_usuario}.

REGRAS OBRIGATÓRIAS:
1. Baseie suas respostas EXCLUSIVAMENTE nos dados do contexto fornecido abaixo.
2. NUNCA invente valores, rentabilidades, transações ou saldos não presentes nos dados.
3. Se não tiver uma informação, diga com franqueza: "Não tenho essa informação nos seus dados, mas posso te ajudar com..."
4. Seja PROATIVO: ao responder sobre gastos ou saldos, mencione o impacto nas metas e sugira próximos passos.
5. Use linguagem semi-informal, clara e acessível, evitando termos complicados sem explicação.
6. Nunca julgue gastos; apresente os dados com gentileza e indique oportunidades de melhoria.
7. Ao recomendar produtos, mencione o nível de risco e avise que é uma orientação que não substitui consultoria certificada.
8. Se a pergunta for fora de finanças, reconheça e redirecione gentilmente.
9. Use emojis com moderação para tornar a conversa amigável 💚.
10. Finalize respostas com uma pergunta ou sugestão proativa.
11. Formate valores financeiros sempre em R$ com duas casas decimais (ex: R$ 5.000,00). NUNCA utilize marcações ou símbolos de fórmula LaTeX.

{contexto}
"""


# ──────────────────────────────────────────────
# Utilitário de Formatação de Texto
# ──────────────────────────────────────────────
def formatar_para_markdown(texto: str) -> str:
    """Escapa cifras $ para impedir que o Streamlit formate valores em blocos verdes de LaTeX/KaTeX."""
    if not texto:
        return ""
    limpo = texto.replace(r"\$", "$")
    return limpo.replace("$", r"\$")


# ──────────────────────────────────────────────
# Listagem e Inicialização do modelo Gemini
# ──────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def listar_modelos_disponiveis(api_key):
    """Lista dinamicamente os modelos suportados pela API Key informada."""
    padrao = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash-8b",
        "gemini-1.5-pro",
        "gemini-2.0-flash",
        "gemini-2.0-flash-exp",
        "gemini-pro",
    ]
    if not api_key:
        return padrao
    try:
        genai.configure(api_key=api_key)
        modelos_api = []
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                modelos_api.append(m.name.replace("models/", ""))
        if modelos_api:
            return modelos_api
    except Exception:
        pass
    return padrao


def inicializar_modelo(api_key, system_prompt, model_name="gemini-1.5-flash"):
    genai.configure(api_key=api_key)
    generation_config = genai.types.GenerationConfig(
        temperature=0.3,
        max_output_tokens=1000,
    )
    clean_name = model_name.replace("models/", "") if model_name else "gemini-1.5-flash"
    model = genai.GenerativeModel(
        model_name=clean_name,
        system_instruction=system_prompt,
        generation_config=generation_config,
    )
    return model


# ──────────────────────────────────────────────
# Modal de Configurações e Gerenciador de Dados
# ──────────────────────────────────────────────
@st.dialog("⚙️ Configurações e Gerenciador de Dados", width="large")
def modal_configuracoes():
    perfil = st.session_state.perfil
    tab_transacoes, tab_perfil = st.tabs(["💸 Transações (Entradas e Saídas)", "👤 Perfil Financeiro"])

    with tab_transacoes:
        st.markdown("#### ➕ Inserir Nova Movimentação")
        with st.form("form_nova_transacao", clear_on_submit=True):
            c_data, c_tipo, c_cat, c_val = st.columns([1.5, 1.5, 2, 2])
            with c_data:
                nova_data = st.date_input("Data", value=date.today()).strftime("%Y-%m-%d")
            with c_tipo:
                novo_tipo = st.selectbox("Tipo", ["saida", "entrada"], format_func=lambda x: "🔴 Saída (Despesa)" if x == "saida" else "🟢 Entrada (Receita)")
            with c_cat:
                categorias_padrao = ["alimentacao", "moradia", "transporte", "saude", "lazer", "receita", "educacao", "outros"]
                nova_categoria = st.selectbox("Categoria", categorias_padrao)
            with c_val:
                novo_valor = st.number_input("Valor (R$)", min_value=0.01, step=10.0, format="%.2f")

            c_desc, c_btn = st.columns([3, 1])
            with c_desc:
                nova_desc = st.text_input("Descrição", placeholder="Ex: Mercado Semanal, Freelance, Farmácia...")
            with c_btn:
                st.write("")
                st.write("")
                btn_inserir = st.form_submit_button("➕ Inserir Movimento", use_container_width=True)

            if btn_inserir:
                if nova_desc.strip():
                    novo_item = pd.DataFrame([{
                        "data": nova_data,
                        "descricao": nova_desc.strip(),
                        "categoria": nova_categoria,
                        "valor": float(novo_valor),
                        "tipo": novo_tipo,
                    }])
                    st.session_state.transacoes = pd.concat([st.session_state.transacoes, novo_item], ignore_index=True)
                    if "chat_session" in st.session_state:
                        del st.session_state["chat_session"]
                    st.success(f"✅ Movimentação '{nova_desc}' adicionada com sucesso!")
                    st.rerun()
                else:
                    st.error("Por favor, preencha a descrição da movimentação.")

        st.markdown("---")
        st.markdown("#### ✏️ Editar Tabela de Transações Diretamente")
        st.caption("Você pode alterar qualquer célula, adicionar novas linhas no fim da tabela ou selecionar linhas e teclar `Delete`:")

        df_editado = st.data_editor(
            st.session_state.transacoes,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "data": st.column_config.TextColumn("Data (AAAA-MM-DD)"),
                "descricao": st.column_config.TextColumn("Descrição"),
                "categoria": st.column_config.SelectboxColumn("Categoria", options=["alimentacao", "moradia", "transporte", "saude", "lazer", "receita", "educacao", "outros"]),
                "valor": st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f", min_value=0.0),
                "tipo": st.column_config.SelectboxColumn("Tipo", options=["entrada", "saida"]),
            },
            key="editor_transacoes",
        )

        col_salvar, col_reset, _ = st.columns([2, 2, 4])
        with col_salvar:
            if st.button("💾 Salvar Alterações da Tabela", use_container_width=True):
                st.session_state.transacoes = df_editado
                salvar_transacoes_disco(df_editado)
                if "chat_session" in st.session_state:
                    del st.session_state["chat_session"]
                st.success("Tabela salva e atualizada com sucesso!")
                st.rerun()

        with col_reset:
            if st.button("🔄 Restaurar Dados Originais do CSV", use_container_width=True):
                st.session_state.transacoes = carregar_transacoes_disco()
                if "chat_session" in st.session_state:
                    del st.session_state["chat_session"]
                st.info("Dados restaurados para o arquivo original!")
                st.rerun()

    with tab_perfil:
        st.markdown("#### ⚙️ Editar Perfil do Cliente")
        with st.form("form_perfil"):
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                novo_salario = st.number_input("Renda Mensal (R$)", value=float(perfil.get("renda_mensal", 5000.0)), step=100.0)
                nova_reserva = st.number_input("Reserva Atual (R$)", value=float(perfil.get("reserva_emergencia_atual", 10000.0)), step=500.0)
            with c_p2:
                perfis_opcoes = ["conservador", "moderado", "arrojado"]
                idx_perfil = perfis_opcoes.index(perfil.get("perfil_investidor", "moderado")) if perfil.get("perfil_investidor") in perfis_opcoes else 1
                novo_tipo_perfil = st.selectbox("Perfil de Investidor", perfis_opcoes, index=idx_perfil)
                aceita_risco_novo = st.checkbox("Aceita Alto Risco?", value=perfil.get("aceita_risco", False))

            btn_salvar_perfil = st.form_submit_button("Salvar Perfil 👤")
            if btn_salvar_perfil:
                perfil["renda_mensal"] = float(novo_salario)
                perfil["reserva_emergencia_atual"] = float(nova_reserva)
                perfil["perfil_investidor"] = novo_tipo_perfil
                perfil["aceita_risco"] = aceita_risco_novo
                st.session_state.perfil = perfil
                salvar_perfil_disco(perfil)
                if "chat_session" in st.session_state:
                    del st.session_state["chat_session"]
                st.success("Perfil atualizado!")
                st.rerun()


# ──────────────────────────────────────────────
# Interface Streamlit
# ──────────────────────────────────────────────
def main():
    # Inicialização dos dados na sessão
    if "transacoes" not in st.session_state:
        try:
            st.session_state.transacoes = carregar_transacoes_disco()
        except Exception as e:
            st.error(f"❌ Erro ao carregar transacoes.csv: {e}")
            return

    if "perfil" not in st.session_state:
        try:
            st.session_state.perfil = carregar_perfil_disco()
        except Exception as e:
            st.error(f"❌ Erro ao carregar perfil_investidor.json: {e}")
            return

    try:
        produtos = carregar_produtos()
        historico = carregar_historico()
    except Exception as e:
        st.error(f"❌ Erro ao carregar base de conhecimento: {e}")
        return

    transacoes = st.session_state.transacoes
    perfil = st.session_state.perfil

    # Cálculo dinâmico das métricas
    entradas_total = float(transacoes[transacoes["tipo"] == "entrada"]["valor"].sum())
    saidas_total = float(transacoes[transacoes["tipo"] == "saida"]["valor"].sum())
    saldo_disponivel = entradas_total - saidas_total

    # ── Barra Lateral ──
    with st.sidebar:
        st.title("💚 Burry")
        st.caption("Assistente Financeiro Inteligente · Desenvolvido por Roz")
        st.divider()

        api_key = st.text_input(
            "🔑 Google Gemini API Key",
            type="password",
            placeholder="Cole sua chave aqui...",
            help="Obtenha grátis em: https://aistudio.google.com/app/apikey",
        )
        if not api_key:
            st.info("Insira sua API Key para ativar o Burry.")
        else:
            modelos_disponiveis = listar_modelos_disponiveis(api_key)
            default_idx = 0
            for pref in ["gemini-1.5-flash-latest", "gemini-1.5-flash", "gemini-2.0-flash", "gemini-pro"]:
                if pref in modelos_disponiveis:
                    default_idx = modelos_disponiveis.index(pref)
                    break

            modelo_escolhido = st.selectbox(
                "🤖 Versão do Modelo",
                options=modelos_disponiveis,
                index=default_idx,
                help="Selecione a versão do Gemini compatível com sua chave de API.",
            )

            if st.session_state.get("modelo_ativo") != modelo_escolhido:
                st.session_state["modelo_ativo"] = modelo_escolhido
                if "chat_session" in st.session_state:
                    del st.session_state["chat_session"]

        st.divider()

        # Resumo Financeiro em Tempo Real
        st.subheader("📊 Resumo Financeiro")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Entradas", f"R$ {entradas_total:,.2f}")
        col_m2.metric("Saídas", f"R$ {saidas_total:,.2f}", delta_color="off")
        
        delta_label = "positivo" if saldo_disponivel >= 0 else "negativo"
        st.metric(
            "Saldo Disponível",
            f"R$ {saldo_disponivel:,.2f}",
            delta=f"{delta_label.capitalize()}" if saldo_disponivel != 0 else None,
            delta_color="normal" if saldo_disponivel >= 0 else "inverse",
        )

        st.write("")
        if st.button("⚙️ Configurações / Editar Dados", use_container_width=True):
            modal_configuracoes()

        if "nome_usuario" in st.session_state:
            st.divider()
            st.subheader(f"👤 {st.session_state.nome_usuario}")
            st.write(f"**Perfil:** {str(perfil.get('perfil_investidor', 'moderado')).capitalize()}")
            st.write(f"**Renda Mensal:** R$ {perfil.get('renda_mensal', 0.0):,.2f}")

            # Metas
            st.markdown("**🎯 Metas Cadastradas:**")
            for meta in perfil.get("metas", []):
                progresso = 0.0
                if "emergência" in meta["meta"].lower() and meta["valor_necessario"] > 0:
                    progresso = perfil.get("reserva_emergencia_atual", 0.0) / meta["valor_necessario"]
                st.write(f"- {meta['meta']} ({meta['prazo']})")
                st.progress(min(progresso, 1.0))

            st.divider()
            if st.button("🔄 Reiniciar Sessão", use_container_width=True):
                st.session_state.clear()
                st.rerun()

    # ── Cabeçalho Principal ──
    st.title("💬 Burry – Seu Consultor Financeiro")

    if not api_key:
        st.warning("⚠️ Insira sua **Google Gemini API Key** na barra lateral para começar a usar o app.")
        st.stop()

    # ── Tela de Boas-vindas (Pergunta o Nome) ──
    if "nome_usuario" not in st.session_state:
        st.markdown("---")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown("### 👋 Olá! Seja bem-vindo(a)!")
            st.write("Antes de começarmos a analisar suas finanças, me conta:")
            with st.form("form_nome"):
                nome_input = st.text_input(
                    "Como posso te chamar?",
                    placeholder="Ex: João, Maria, Neto...",
                    max_chars=40,
                )
                enviado = st.form_submit_button("Entrar no Burry 💚", use_container_width=True)

            if enviado:
                if nome_input.strip():
                    st.session_state.nome_usuario = nome_input.strip()
                    st.rerun()
                else:
                    st.error("Por favor, digite seu nome para continuar.")
        st.stop()

    nome = st.session_state.nome_usuario
    st.caption(f"Desenvolvido por Roz · Olá, {nome}! 👋")

    # ── 1. Resumo Financeiro em Destaque ──
    st.markdown("### 📊 Resumo Financeiro")
    col_c1, col_c2, col_c3 = st.columns(3)
    col_c1.metric("🟢 Total Entradas", f"R$ {entradas_total:,.2f}")
    col_c2.metric("🔴 Total Saídas", f"R$ {saidas_total:,.2f}")
    delta_rotulo = "Saldo Positivo" if saldo_disponivel >= 0 else "Saldo Negativo"
    col_c3.metric(
        "💰 Saldo Disponível",
        f"R$ {saldo_disponivel:,.2f}",
        delta=delta_rotulo if saldo_disponivel != 0 else None,
        delta_color="normal" if saldo_disponivel >= 0 else "inverse",
    )
    st.markdown("---")

    # ── Inicialização do Chat com o Burry ──
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_session" not in st.session_state:
        contexto = montar_contexto(st.session_state.perfil, st.session_state.transacoes, produtos, historico, nome)
        system_prompt = criar_system_prompt(contexto, nome)
        modelo_selecionado = st.session_state.get("modelo_ativo", "gemini-1.5-flash-latest")
        try:
            model = inicializar_modelo(api_key, system_prompt, model_name=modelo_selecionado)
            st.session_state.chat_session = model.start_chat(history=[])
            
            # Mensagem inicial com os dados recalculados em tempo real
            boas_vindas = (
                f"Oi, {nome}! 👋 Que bom falar com você!\n\n"
                f"Estou com seu histórico atualizado em mãos:\n"
                f"- 🟢 **Entradas:** R$ {entradas_total:,.2f}\n"
                f"- 🔴 **Saídas registradas:** R$ {saidas_total:,.2f}\n"
                f"- 💰 **Saldo disponível:** R$ {saldo_disponivel:,.2f}\n\n"
                f"Sua reserva de emergência está em "
                f"**{(st.session_state.perfil.get('reserva_emergencia_atual', 0.0) / st.session_state.perfil['metas'][0]['valor_necessario'] * 100):.0f}%** da meta! 🎯\n\n"
                f"Você pode usar o botão de configurações na barra lateral para adicionar novas despesas/receitas quando quiser. "
                f"Como posso te ajudar a planejar seu dinheiro hoje? 💚"
            )
            st.session_state.messages = [{"role": "assistant", "content": boas_vindas}]
        except Exception as e:
            st.error(f"❌ Erro ao conectar com o modelo `{modelo_selecionado}`: {e}\n\n👉 **Dica:** Tente selecionar outra versão no menu **'🤖 Versão do Modelo'** na barra lateral esquerda.")
            st.stop()

    # Exibir histórico de mensagens
    for msg in st.session_state.messages:
        avatar = "💚" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(formatar_para_markdown(msg["content"]))

    # Input do Usuário
    if prompt := st.chat_input(f"Pergunte ao Burry sobre seus gastos, saldo e investimentos..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(formatar_para_markdown(prompt))

        with st.chat_message("assistant", avatar="💚"):
            try:
                response = st.session_state.chat_session.send_message(prompt, stream=True)

                def gerar_resposta():
                    for chunk in response:
                        if chunk.text:
                            yield chunk.text.replace("$", r"\$")

                resposta = st.write_stream(gerar_resposta())
            except Exception as e:
                mod = st.session_state.get("modelo_ativo", "selecionado")
                resposta = (
                    f"Ops! Tive um problema ao responder com o modelo `{mod}`: {e}\n\n"
                    f"👉 **Dica:** Tente selecionar outra versão no menu **'🤖 Versão do Modelo'** na barra lateral esquerda (ex: `gemini-1.5-flash-latest`, `gemini-2.0-flash` ou `gemini-pro`)."
                )
                st.markdown(resposta)

            st.session_state.messages.append({"role": "assistant", "content": resposta})


if __name__ == "__main__":
    main()
