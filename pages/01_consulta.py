import streamlit as st
import pandas as pd
from services.equipment_service import listar_equipamentos

st.header("📋 Consulta de Equipamentos")

equipamentos = listar_equipamentos()

if not equipamentos:
    st.info("Nenhum equipamento cadastrado ainda. Acesse **Cadastro Técnico** para adicionar.")
    st.stop()

df = pd.DataFrame(equipamentos)[["id","tag","modelo","fabricante","potencia_kw","tensao_v","criado_em"]]
df.columns = ["ID","TAG","Modelo","Fabricante","Potência (kW)","Tensão (V)","Cadastrado em"]
df["Cadastrado em"] = pd.to_datetime(df["Cadastrado em"]).dt.strftime("%d/%m/%Y %H:%M")

st.dataframe(df.drop(columns=["ID"]), use_container_width=True, hide_index=True)

st.divider()
st.subheader("🔍 Abrir ficha técnica")

opcoes = {f"{e['tag']} — {e['modelo']}": e["id"] for e in equipamentos}
selecionado = st.selectbox("Selecione o equipamento:", list(opcoes.keys()))

if selecionado:
    eq_id = opcoes[selecionado]
    eq = next(e for e in equipamentos if e["id"] == eq_id)

    col1, col2, col3 = st.columns(3)
    col1.metric("TAG", eq["tag"])
    col2.metric("Potência", f"{eq['potencia_kw']} kW")
    col3.metric("Tensão", f"{eq['tensao_v']} V")

    with st.expander("📄 Ficha Técnica Completa", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Modelo:** {eq['modelo']}")
            st.write(f"**Fabricante:** {eq['fabricante']}")
            st.write(f"**Nº de Série:** {eq.get('num_serie', '—')}")
            st.write(f"**Ano de Fabricação:** {eq.get('ano_fabricacao', '—')}")
        with c2:
            st.write(f"**Potência:** {eq['potencia_kw']} kW")
            st.write(f"**Tensão:** {eq['tensao_v']} V")
            st.write(f"**Corrente Nominal:** {eq.get('corrente_a', '—')} A")
            st.write(f"**Rotação Nominal:** {eq.get('rotacao_rpm', '—')} RPM")

        if eq.get("observacoes"):
            st.write(f"**Observações:** {eq['observacoes']}")