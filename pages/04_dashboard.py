import streamlit as st
import plotly.graph_objects as go
from services.equipment_service import listar_equipamentos
from services.data_generator import (
    gerar_historico, get_leitura_atual,
    get_status, get_cor_status, LIMITES
)

st.header("📈 Dashboard de Telemetria")

equipamentos = listar_equipamentos()
if not equipamentos:
    st.info("Nenhum equipamento cadastrado.")
    st.stop()

tags = [e["tag"] for e in equipamentos]
tag_default = st.session_state.get("tag_dashboard", tags[0])
idx = tags.index(tag_default) if tag_default in tags else 0

col_sel, col_per = st.columns([2, 1])
tag     = col_sel.selectbox("Motor (TAG)", tags, index=idx)
periodo = col_per.slider("Período (dias)", min_value=1, max_value=7, value=3)

eq      = next(e for e in equipamentos if e["tag"] == tag)
leitura = get_leitura_atual(tag)
df      = gerar_historico(tag, dias=periodo)

# ── Cards de status ──────────────────────────────────────────────────
st.divider()
st.subheader("🔴 Status Operacional em Tempo Real")

c1, c2, c3, c4 = st.columns(4)

def card_status(col, label, valor, unidade, sensor):
    status = get_status(valor, sensor)
    cor    = get_cor_status(status)
    col.markdown(f"""
    <div style="border-left: 5px solid {cor}; background: #12121f;
                border-radius: 8px; padding: 14px; margin-bottom: 4px;">
        <p style="color: #999; font-size: 12px; margin: 0;">{label}</p>
        <h2 style="color: white; margin: 4px 0;">{valor} {unidade}</h2>
        <span style="background: {cor}; color: white; padding: 2px 10px;
               border-radius: 20px; font-size: 12px; font-weight: bold;">{status}</span>
    </div>
    """, unsafe_allow_html=True)

card_status(c1, "🌡️ Temperatura",  leitura["temperatura"], "°C",   "temperatura")
card_status(c2, "〰️ Vibração",     leitura["vibracao"],    "mm/s", "vibracao")
card_status(c3, "⚡ Corrente",      leitura["corrente"],    "A",    "corrente")
c4.markdown(f"""
<div style="border-left: 5px solid #3498db; background: #12121f;
            border-radius: 8px; padding: 14px;">
    <p style="color: #999; font-size: 12px; margin: 0;">🕐 Última Leitura</p>
    <p style="color: white; font-size: 15px; margin: 6px 0;">{leitura['timestamp']}</p>
    <span style="background: #3498db; color: white; padding: 2px 10px;
           border-radius: 20px; font-size: 12px;">● ONLINE</span>
</div>
""", unsafe_allow_html=True)

# ── Gráficos de séries temporais ─────────────────────────────────────
st.divider()
st.subheader("Histórico de Telemetria")

def grafico(df, coluna, label, unidade, cor, sensor):
    lim = LIMITES[sensor]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["timestamp"], y=df[coluna],
        mode="lines", name=label,
        line=dict(color=cor, width=1.8),
        fill="tozeroy", fillcolor=f"rgba{tuple(list(bytes.fromhex(cor.lstrip('#'))) + [30])}"
    ))
    fig.add_hline(
        y=lim["alerta"], line_dash="dash", line_color="#f39c12", line_width=1.5,
        annotation_text="⚠ Alerta", annotation_position="top right",
        annotation_font_color="#f39c12"
    )
    fig.add_hline(
        y=lim["critico"], line_dash="dash", line_color="#e74c3c", line_width=1.5,
        annotation_text="🔴 Crítico", annotation_position="top right",
        annotation_font_color="#e74c3c"
    )
    fig.update_layout(
        title=dict(text=f"{label} ({unidade})", font=dict(color="white", size=14)),
        height=260,
        plot_bgcolor="#0e0e1a",
        paper_bgcolor="#0e0e1a",
        font=dict(color="#ccc"),
        xaxis=dict(gridcolor="#222", showgrid=True),
        yaxis=dict(gridcolor="#222", showgrid=True),
        margin=dict(t=40, b=20, l=10, r=10),
        showlegend=False,
    )
    return fig

col_g1, col_g2 = st.columns(2)
with col_g1:
    st.plotly_chart(grafico(df, "temperatura", "Temperatura", "°C",   "#e74c3c", "temperatura"), use_container_width=True)
with col_g2:
    st.plotly_chart(grafico(df, "vibracao",    "Vibração",    "mm/s", "#9b59b6", "vibracao"),    use_container_width=True)

st.plotly_chart(grafico(df, "corrente", "Corrente", "A", "#3498db", "corrente"), use_container_width=True)

# ── Ficha + imagem da placa ───────────────────────────────────────────
st.divider()
st.subheader("Placa do Motor — Visão Computacional")

col_img, col_ficha = st.columns([1, 2])

with col_img:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/WEG_Motor_nameplate.jpg/320px-WEG_Motor_nameplate.jpg",
        caption="Placa WEG W22 — extraída via visão computacional",
        use_container_width=True
    )

with col_ficha:
    st.markdown(f"""
    | Campo | Valor |
    |---|---|
    | **TAG** | {eq.get('tag', '—')} |
    | **Modelo** | {eq.get('modelo', '—')} |
    | **Fabricante** | {eq.get('fabricante', '—')} |
    | **Potência** | {eq.get('potencia_kw', '—')} kW |
    | **Tensão** | {eq.get('tensao_v', '—')} V |
    | **Corrente Nominal** | {eq.get('corrente_a', '—')} A |
    | **Rotação Nominal** | {eq.get('rotacao_rpm', '—')} RPM |
    | **Nº de Série** | {eq.get('num_serie', '—')} |
    """)