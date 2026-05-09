import streamlit as st
from services.equipment_service import cadastrar_equipamento

st.header("Cadastro Técnico de Equipamento")
st.caption("Preencha os dados da ficha técnica do equipamento.")

with st.form("form_cadastro", clear_on_submit=True):
    st.subheader("Identificação")
    c1, c2 = st.columns(2)
    tag            = c1.text_input("TAG de Identificação *", placeholder="EQ-001")
    modelo         = c2.text_input("Modelo *",               placeholder="WEG W22")
    fabricante     = c1.text_input("Fabricante *",            placeholder="WEG")
    num_serie      = c2.text_input("Nº de Série",             placeholder="SN-2024-001")
    ano_fabricacao = c1.number_input("Ano de Fabricação", min_value=1950, max_value=2030, value=2023, step=1)

    st.divider()
    st.subheader("Dados Elétricos")
    c3, c4 = st.columns(2)
    potencia_kw    = c3.number_input("Potência (kW) *",       min_value=0.0, step=0.1, format="%.2f")
    tensao_v       = c4.selectbox("Tensão (V) *",             [127, 220, 380, 440, 690])
    corrente_a     = c3.number_input("Corrente Nominal (A)",  min_value=0.0, step=0.1, format="%.2f")
    rotacao_rpm    = c4.number_input("Rotação Nominal (RPM)", min_value=0,   step=10,  value=1800)
    fator_potencia = c3.slider("Fator de Potência (cos φ)",   0.0, 1.0, 0.92, step=0.01)

    st.divider()
    observacoes = st.text_area("Observações", placeholder="Informações adicionais sobre o equipamento...")

    submitted = st.form_submit_button("💾 Cadastrar Equipamento", type="primary", use_container_width=True)

if submitted:
    erros = []
    if not tag:          erros.append("TAG de Identificação é obrigatório.")
    if not modelo:       erros.append("Modelo é obrigatório.")
    if not fabricante:   erros.append("Fabricante é obrigatório.")
    if potencia_kw <= 0: erros.append("Potência deve ser maior que zero.")

    if erros:
        for e in erros:
            st.error(e)
    else:
        dados = {
            "tag": tag, "modelo": modelo, "fabricante": fabricante,
            "num_serie": num_serie, "ano_fabricacao": ano_fabricacao,
            "potencia_kw": potencia_kw, "tensao_v": tensao_v,
            "corrente_a": corrente_a, "rotacao_rpm": rotacao_rpm,
            "fator_potencia": fator_potencia, "observacoes": observacoes,
        }
        eq = cadastrar_equipamento(dados)
        st.success(f"✅ Equipamento **{eq['tag']}** cadastrado com sucesso! ID: `{eq['id']}`")
        st.balloons()