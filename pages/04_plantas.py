import streamlit as st
from services.equipment_service import listar_equipamentos
from services.data_generator import PLANTAS, get_leitura_atual, get_status, get_cor_status

st.header("🏭 Navegação por Planta / Área")
st.caption("Selecione a planta e a área para visualizar o estado dos equipamentos.")

col_p, col_a = st.columns(2)
planta = col_p.selectbox("Planta", list(PLANTAS.keys()))
area   = col_a.selectbox("Área",   PLANTAS[planta])

st.divider()
st.subheader(f"Equipamentos — {planta} › {area}")

equipamentos = listar_equipamentos()

if not equipamentos:
    st.info("Nenhum equipamento cadastrado. Acesse **Cadastro Técnico** para adicionar.")
    st.stop()

# Exibe cards para cada equipamento (usa todos pois localização é simulada)
cols = st.columns(min(len(equipamentos), 3))

for idx, eq in enumerate(equipamentos):
    leitura = get_leitura_atual(eq["tag"])
    status  = get_status(leitura["temperatura"], "temperatura")
    cor     = get_cor_status(status)

    with cols[idx % 3]:
        st.markdown(f"""
        <div style="border: 2px solid {cor}; border-radius: 12px; padding: 18px;
                    text-align: center; background: #1a1a2e; margin-bottom: 12px;">
            <p style="color: #aaa; font-size: 12px; margin: 0;">TAG</p>
            <h3 style="color: white; margin: 4px 0;">{eq['tag']}</h3>
            <p style="color: #ccc; font-size: 13px; margin: 0;">{eq['modelo']} · {eq['fabricante']}</p>
            <hr style="border-color: #333; margin: 10px 0;">
            <h4 style="color: {cor}; margin: 6px 0;">⬤ {status}</h4>
            <p style="color: #ddd; margin: 4px 0;">🌡️ {leitura['temperatura']} °C</p>
            <p style="color: #ddd; margin: 4px 0;">〰️ {leitura['vibracao']} mm/s</p>
            <p style="color: #ddd; margin: 4px 0;">⚡ {leitura['corrente']} A</p>
            <p style="color: #888; font-size: 11px; margin-top: 8px;">{leitura['timestamp']}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("📊 Ver Dashboard", key=f"dash_{eq['tag']}", use_container_width=True):
            st.session_state["tag_dashboard"] = eq["tag"]
            st.switch_page("pages/05_dashboard.py")