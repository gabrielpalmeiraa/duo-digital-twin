import streamlit as st

pages = [
    st.Page("pages/00_painel_alertas.py", title="Painel de Alertas",       icon="🚨"),
    st.Page("pages/01_consulta.py",       title="Consulta de Equipamentos", icon="📋"),
    st.Page("pages/02_cadastro.py",       title="Cadastro Técnico",         icon="➕"),
    st.Page("pages/03_dados_brutos.py",   title="Visualização de Dados",    icon="📊"),
    st.Page("pages/04_plantas.py",        title="Navegação por Planta",     icon="🏭"),
    st.Page("pages/05_dashboard.py",      title="Dashboard de Telemetria",  icon="📈"),
]

pg = st.navigation(pages)

st.set_page_config(
    page_title="DUO — Gêmeo Digital do Café",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.image("https://img.icons8.com/color/96/coffee-bean.png", width=60)
    st.title("DUO")
    st.caption("Gêmeo Digital para Beneficiamento do Café")
    st.divider()
    st.caption("Sprint 3 · FIAP · Forzy Challenge")

pg.run()