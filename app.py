import streamlit as st
from gmail_client import get_gmail_service, fetch_emails
from llm_processor import classify_email, generate_draft, summarize_inbox
from cache import get_cached_analysis, save_analysis

# ── CONFIG ───────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="E-mail Assistant",
    page_icon="📬",
    layout="wide"
)

URGENCY_CONFIG = {
    "alta":  {"icon": "🔴", "label": "Alta",  "color": "#FF4B4B"},
    "media": {"icon": "🟡", "label": "Média", "color": "#FFA500"},
    "baixa": {"icon": "🟢", "label": "Baixa", "color": "#00C853"},
}

# Inicializa todas as chaves com valores padrão corretos.
# 'processed' começa como False (não None) — semanticamente correto para um booleano.
# 'filter_urgency' e 'filter_category' já começam preenchidos para evitar KeyError
# na área principal antes da sidebar renderizar os multiselects.
defaults = {
    'emails': None,
    'service': None,
    'processed': False,
    'inbox_summary': None,
    'filter_urgency': ["alta", "media", "baixa"],
    'filter_category': ["trabalho", "pessoal", "financeiro", "spam", "outro"]
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ── SIDEBAR ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("📬 Email Assistant")
    st.caption("Triagem inteligente com IA")
    st.divider()

    if st.button("🔗 Conectar ao Gmail", use_container_width=True):
        with st.spinner("Autenticando..."):
            st.session_state['service'] = get_gmail_service()
        st.success("Conectado!")

    if st.session_state['service']:
        st.divider()

        n_emails = st.number_input(
            "Quantos e-mails você quer carregar?",
            min_value=2, max_value=50, value=10, step=1
        )

        if st.button("📥 Carregar e Analisar", use_container_width=True, type="primary"):
            with st.spinner("Buscando e-mails no Gmail..."):
                emails = fetch_emails(st.session_state['service'], max_results=n_emails)

            progress = st.progress(0, text="Analisando com IA...")
            cached_count = 0

            for i, email in enumerate(emails):
                cached = get_cached_analysis(email['id'])

                if cached:
                    email['analysis'] = cached
                    cached_count += 1
                else:
                    email['analysis'] = classify_email(email)
                    save_analysis(email['id'], email['analysis'])

                progress.progress(
                    (i + 1) / len(emails),
                    text=f"Analisando {i+1}/{len(emails)}... ({cached_count} do cache)"
                )

            # Fora do for — só executa após todos os e-mails serem processados
            st.session_state['emails'] = emails
            st.session_state['processed'] = True

            with st.spinner("Gerando resumo da caixa de entrada..."):
                st.session_state['inbox_summary'] = summarize_inbox(emails)

            st.rerun()

        st.divider()

        if st.session_state['processed']:
            st.subheader("Filtros")

            filter_urgency = st.multiselect(
                "Urgência",
                options=["alta", "media", "baixa"],
                default=["alta", "media", "baixa"],
                format_func=lambda x: f"{URGENCY_CONFIG[x]['icon']} {URGENCY_CONFIG[x]['label']}"
            )

            filter_category = st.multiselect(
                "Categoria",
                options=["trabalho", "pessoal", "financeiro", "spam", "outro"],
                default=["trabalho", "pessoal", "financeiro", "spam", "outro"]
            )

            st.session_state['filter_urgency'] = filter_urgency
            st.session_state['filter_category'] = filter_category

# ── MAIN AREA ────────────────────────────────────────────────────────────────

if not st.session_state['service']:
    st.title("📬 Assistente de Triagem de E-mails")
    st.info("Conecte sua conta do Gmail na barra lateral para começar.")
    st.stop()

if not st.session_state['processed']:
    st.title("📬 Assistente de Triagem de E-mails")
    st.info("Clique em **Carregar e Analisar** para processar sua caixa de entrada.")
    st.stop()

emails = st.session_state['emails']
filter_urgency = st.session_state.get('filter_urgency', ["alta", "media", "baixa"])
filter_category = st.session_state.get('filter_category', ["trabalho", "pessoal", "financeiro", "spam", "outro"])

filtered = [
    e for e in emails
    if e.get('analysis', {}).get('urgency') in filter_urgency
    and e.get('analysis', {}).get('category') in filter_category
]

# ── Cabeçalho com métricas ──

st.title("📬 Sua Caixa de Entrada")

col1, col2, col3, col4 = st.columns(4)
altas  = sum(1 for e in emails if e.get('analysis', {}).get('urgency') == 'alta')
medias = sum(1 for e in emails if e.get('analysis', {}).get('urgency') == 'media')
baixas = sum(1 for e in emails if e.get('analysis', {}).get('urgency') == 'baixa')

col1.metric("📧 Total",          len(emails))
col2.metric("🔴 Alta urgência",  altas)
col3.metric("🟡 Média urgência", medias)
col4.metric("🟢 Baixa urgência", baixas)

st.divider()

# ── Resumo inteligente ──

if st.session_state['inbox_summary']:
    with st.expander("🧠 Resumo Inteligente da Caixa de Entrada", expanded=True):
        st.write(st.session_state['inbox_summary'])

st.divider()
st.subheader(f"E-mails ({len(filtered)} exibidos)")

# ── Lista de e-mails ─────────────────────────────────────────────────────────

for email in filtered:
    analysis = email.get('analysis', {})
    urgency  = analysis.get('urgency', 'baixa')
    cfg      = URGENCY_CONFIG.get(urgency, URGENCY_CONFIG['baixa'])

    expander_title = (
        f"{cfg['icon']} {email['subject']}  "
        f"· {email['from'].split('<')[0].strip()}"
    )

    with st.expander(expander_title):
        info_col, action_col = st.columns([2, 1])

        with info_col:
            st.markdown(f"**De:** {email['from']}")
            st.markdown(f"**Data:** {email['date']}")
            st.markdown(f"**Resumo:** {analysis.get('summary', '')}")
            st.caption(f"💭 *{analysis.get('reasoning', '')}*")

        with action_col:
            color = cfg['color']
            label = cfg['label']
            st.markdown(
                f'<span style="background:{color};color:white;'
                f'padding:3px 10px;border-radius:12px;font-size:13px;">'
                f'{cfg["icon"]} {label}</span>',
                unsafe_allow_html=True
            )
            st.markdown(f"**Categoria:** `{analysis.get('category', '')}`")

        st.divider()

        if st.button("✍️ Gerar rascunho de resposta", key=f"draft_{email['id']}"):
            with st.spinner("Gerando rascunho..."):
                draft = generate_draft(email, analysis)

            st.text_area(
                "Rascunho sugerido:",
                value=draft,
                height=150,
                key=f"textarea_{email['id']}"
            )