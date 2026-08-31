"""
Componentes de UI reutilizáveis para o Painel de Alertas e Estados (Sprint 3).
Mantidos isolados das páginas para permitir reaproveitamento (ex.: dashboard,
navegação por planta) e facilitar manutenção/evolução visual.
"""

import streamlit as st

ICONE_PRIORIDADE = {"alta": "🚨", "media": "⚠️", "baixa": "✅"}


def badge_status(status: str, cor: str) -> str:
    return (
        f'<span style="background:{cor}; color:white; padding:2px 12px; '
        f'border-radius:20px; font-size:12px; font-weight:bold; white-space:nowrap;">'
        f'⬤ {status}</span>'
    )


def render_recommendation_card(rec: dict, cor: str):
    """Card de apoio inicial à decisão (recomendação de ação) — largura total, bem visível."""
    icone = ICONE_PRIORIDADE.get(rec["prioridade"], "ℹ️")
    st.markdown(
        f"""
        <div style="background:{cor}22; border:2px solid {cor}; border-radius:10px;
                    padding:14px 18px; margin:10px 0 4px 0;">
            <p style="margin:0; color:{cor}; font-weight:800; font-size:16px;">
                {icone} APOIO À DECISÃO: {rec['titulo']}
            </p>
            <p style="margin:6px 0 0 0; color:#f0f0f0; font-size:14px;">{rec['texto']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_alert_card(alerta: dict, key_prefix: str = "", dashboard_page: str = "pages/05_dashboard.py"):
    """Card completo de alerta: status, resumo NLP e recomendação, com atalho pro dashboard."""
    eq = alerta["equipamento"]
    cor = alerta["cor"]

    st.markdown(
        f"""
        <div style="border-left:6px solid {cor}; background:#141425; border-radius:10px;
                    padding:16px 18px; margin-bottom:6px;">
            <div style="display:flex; justify-content:space-between; align-items:center; gap:10px;">
                <h4 style="margin:0; color:white;">{eq['tag']} — {eq['modelo']}</h4>
                {badge_status(alerta['status'], cor)}
            </div>
            <p style="color:#999; font-size:12px; margin:6px 0 10px 0;">🕐 {alerta['timestamp']}</p>
            <p style="color:#ddd; font-size:14px; margin:0;">
                <b>📝 Resumo (NLP):</b> {alerta['resumo_nlp']}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_recommendation_card(alerta["recomendacao"], cor)

    c1, c2 = st.columns([3, 1])
    with c2:
        if st.button("📊 Ver Dashboard", key=f"{key_prefix}_dash_{eq['tag']}", use_container_width=True):
            st.session_state["tag_dashboard"] = eq["tag"]
            st.switch_page(dashboard_page)
    st.markdown("<div style='margin-bottom:18px;'></div>", unsafe_allow_html=True)


def render_evento_historico(evento: dict):
    """Item de linha do histórico de eventos (mudanças de estado)."""
    cor = evento["cor"]
    st.markdown(
        f"""
        <div style="border-left:4px solid {cor}; padding:8px 14px; margin-bottom:6px;
                    background:#101020; border-radius:6px;">
            <span style="color:#888; font-size:12px;">{evento['timestamp']}</span> —
            <b style="color:white;">{evento['tag']}</b>
            <span style="color:{cor}; font-weight:bold;"> mudou para {evento['status']}</span>
            <p style="color:#aaa; font-size:12px; margin:4px 0 0 0;">{evento['resumo']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
