import streamlit as st
import pandas as pd
import random
from services.equipment_service import listar_equipamentos
from services.data_converter import CONVERSORES, raw_to_volts, raw_to_amperes, raw_to_rpm, raw_to_temperature

st.header("📊 Visualização de Dados Brutos")
st.caption("Converta sinais brutos dos sensores em unidades de engenharia.")

equipamentos = listar_equipamentos()

if not equipamentos:
    st.warning("Nenhum equipamento cadastrado. Cadastre um primeiro.")
    st.stop()

opcoes = {f"{e['tag']} — {e['modelo']}": e for e in equipamentos}
sel = st.selectbox("Equipamento:", list(opcoes.keys()))
eq = opcoes[sel]

st.divider()
tab1, tab2 = st.tabs(["🔢 Conversor Manual", "📈 Simulação de Leitura"])

with tab1:
    st.subheader("Conversão de Sinal Bruto")
    c1, c2 = st.columns([1, 1])
    tipo = c1.selectbox("Tipo de sinal:", list(CONVERSORES.keys()))
    raw  = c2.number_input("Valor bruto (ADC):", min_value=0.0, max_value=4095.0, value=2048.0, step=1.0)

    resultado = CONVERSORES[tipo](raw)
    st.metric(label=f"Resultado — {tipo}", value=resultado)

    with st.expander("ℹ️ Como é feita a conversão?"):
        st.markdown(f"""
        | Parâmetro | Valor |
        |---|---|
        | Sinal bruto | `{raw}` |
        | Tipo | {tipo} |
        | Resultado convertido | **{resultado}** |
        | Referência (Vref) | 5.0 V |
        | Resolução ADC | 12 bits (0–4095) |
        """)

with tab2:
    st.subheader(f"Simulação de Leitura — {eq['tag']}")
    st.caption("Dados simulados para demonstração. Nas próximas sprints virão dos sensores reais.")

    if st.button("🔄 Gerar Nova Leitura", type="primary"):
        leituras = {
            "Tensão (V)":         raw_to_volts(random.uniform(3400, 3800)),
            "Corrente (A)":       raw_to_amperes(random.uniform(2300, 2700)),
            "Rotação (RPM)":      raw_to_rpm(random.randint(28, 32)),
            "Temperatura (°C)":   raw_to_temperature(random.uniform(300, 500)),
        }
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Tensão",      f"{leituras['Tensão (V)']} V")
        col2.metric("Corrente",    f"{leituras['Corrente (A)']} A")
        col3.metric("Rotação",     f"{leituras['Rotação (RPM)']} RPM")
        col4.metric("Temperatura", f"{leituras['Temperatura (°C)']} °C")

        df_sim = pd.DataFrame([{
            "Parâmetro": k,
            "Valor Convertido": v,
            "Raw (simulado)": round(random.uniform(0, 4095), 0)
        } for k, v in leituras.items()])
        st.dataframe(df_sim, use_container_width=True, hide_index=True)