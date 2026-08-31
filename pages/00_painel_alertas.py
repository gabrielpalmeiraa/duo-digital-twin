import time
from datetime import datetime

import streamlit as st

from services.equipment_service import listar_equipamentos
from services.alert_service import obter_alertas
from components.alert_components import render_alert_card, render_evento_historico

st.header("🚨 Painel de Alertas e Estados")
st.caption(
    "Acompanhamento contínuo do estado operacional dos ativos, com resumos gerados "
    "por NLP e recomendações de apoio à decisão para a equipe de manutenção."
)

equipamentos = listar_equipamentos()
if not equipamentos:
    st.info("Nenhum equipamento cadastrado ainda. Acesse **Cadastro Técnico** para adicionar.")
    st.stop()

# ── Estado de sessão ──────────────────────────────────────────────────
if "historico_eventos" not in st.session_state:
    st.session_state["historico_eventos"] = []
if "status_anterior" not in st.session_state:
    st.session_state["status_anterior"] = {}
if "ultima_atualizacao" not in st.session_state:
    st.session_state["ultima_atualizacao"] = None
if "alertas_atual" not in st.session_state:
    st.session_state["alertas_atual"] = None
if "novos_eventos" not in st.session_state:
    st.session_state["novos_eventos"] = []

# ── Controles: atualização manual e automática ────────────────────────
col_btn, col_auto, col_ts = st.columns([1.2, 1.6, 2])
atualizar_clicado = col_btn.button("🔄 Atualizar Painel", type="primary", use_container_width=True)
auto = col_auto.checkbox("⏱️ Atualização automática (15s)", value=False)


def _processar_alertas() -> tuple[list, list]:
    """Reavalia todos os equipamentos e registra no histórico as mudanças de estado."""
    alertas = obter_alertas(equipamentos)
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    novos_eventos = []

    for a in alertas:
        tag = a["equipamento"]["tag"]
        status_ant = st.session_state["status_anterior"].get(tag)
        mudou = status_ant != a["status"]
        if mudou and (status_ant is not None or a["status"] != "NORMAL"):
            evento = {
                "timestamp": agora,
                "tag": tag,
                "status": a["status"],
                "cor": a["cor"],
                "resumo": a["resumo_nlp"],
            }
            st.session_state["historico_eventos"].insert(0, evento)
            novos_eventos.append(evento)
        st.session_state["status_anterior"][tag] = a["status"]

    st.session_state["historico_eventos"] = st.session_state["historico_eventos"][:20]
    st.session_state["ultima_atualizacao"] = agora
    return alertas, novos_eventos


def _deve_atualizar() -> bool:
    if atualizar_clicado or st.session_state["ultima_atualizacao"] is None:
        return True
    if auto:
        decorrido = (
            datetime.now() - datetime.strptime(st.session_state["ultima_atualizacao"], "%d/%m/%Y %H:%M:%S")
        ).total_seconds()
        return decorrido >= 15
    return False


if _deve_atualizar():
    alertas, novos_eventos = _processar_alertas()
    st.session_state["alertas_atual"] = alertas
    st.session_state["novos_eventos"] = novos_eventos
else:
    alertas = st.session_state["alertas_atual"]

col_ts.caption(f"🕐 Última atualização: **{st.session_state['ultima_atualizacao']}**")

# ── Banner de novo alerta (persistente — não some sozinho como um toast) ──
novos_eventos = st.session_state.get("novos_eventos", [])
if novos_eventos:
    for ev in novos_eventos:
        if ev["status"] == "CRÍTICO":
            st.error(f"🚨 **Novo alerta CRÍTICO** — {ev['tag']} mudou para CRÍTICO agora ({ev['timestamp']}).")
        elif ev["status"] == "ALERTA":
            st.warning(f"⚠️ **Novo alerta** — {ev['tag']} mudou para ALERTA agora ({ev['timestamp']}).")
        else:
            st.success(f"✅ **{ev['tag']} normalizou** — voltou para o estado saudável ({ev['timestamp']}).")

st.divider()

# ── Resumo geral ───────────────────────────────────────────────────────
criticos = sum(1 for a in alertas if a["status"] == "CRÍTICO")
em_alerta = sum(1 for a in alertas if a["status"] == "ALERTA")
saudaveis = sum(1 for a in alertas if a["status"] == "NORMAL")

m1, m2, m3 = st.columns(3)
m1.metric("🔴 Críticos", criticos)
m2.metric("🟡 Em Atenção", em_alerta)
m3.metric("🟢 Saudáveis", saudaveis)

st.divider()
st.subheader("Alertas por Equipamento")

for alerta in alertas:
    render_alert_card(alerta, key_prefix="painel")

st.divider()
st.subheader("🕓 Histórico de Eventos")

historico = st.session_state["historico_eventos"]
if not historico:
    st.caption("Nenhuma mudança de estado registrada ainda nesta sessão.")
else:
    for evento in historico:
        render_evento_historico(evento)

# ── Timer de atualização automática ─────────────────────────────────────
if auto:
    time.sleep(1)
    st.rerun()
