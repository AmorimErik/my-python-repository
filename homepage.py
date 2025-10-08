import streamlit as st

col_esq, col_dir = st.columns([1, 1.5])
col_esq.title("Hash&Co")
col_esq.write("#### Bem Vindo, Erik")

button_dashboards = col_esq.button("Dashboards Projetos")
button_indicadores = col_esq.button("Principais Indicadores")

container = col_dir.container(border=True)
container.image("images/time-comunidade.webp")

if button_dashboards:
    st.switch_page("dashboard.py")
if button_indicadores:
    st.switch_page("indicadores.py")
