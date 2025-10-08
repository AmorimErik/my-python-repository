import streamlit as st
import plotly.express as px
from data_loader import carregar_dados


base = carregar_dados()


def criar_card(icone, numero, texto, col_card):
    container = col_card.container(border=True)
    col_esq, col_dir = container.columns([1, 2.5])
    col_esq.image(f"images/{icone}")
    col_dir.write(numero)
    col_dir.write(texto)


col_esq, col_meio, col_dir = st.columns([1, 1, 1])

contrato_andamento = base[base["Status"] == "Em andamento"]
contrato_fechado = base[base["Status"].isin(["Em andamento", "Finalizado"])]

criar_card(
    "oportunidades.png", f"{base["Código Projeto"].count():,}", "Oportunidades", col_esq
)
criar_card(
    "projetos_fechados.png",
    f"{contrato_fechado["Código Projeto"].count():,}",
    "Projetos Fechados",
    col_meio,
)
criar_card(
    "em_andamento.png",
    f"{contrato_andamento["Código Projeto"].count():,}",
    "Em andamento",
    col_dir,
)
criar_card(
    "total_orcado.png",
    f"R$ {contrato_fechado["Valor Orçado"].sum():,}",
    "Total Orçado",
    col_esq,
)
criar_card(
    "total_pago.png",
    f"R$ {contrato_fechado["Valor Negociado"].sum():,}",
    "Total Pago",
    col_meio,
)
criar_card(
    "desconto.png",
    f"R$ {contrato_fechado["Desconto Concedido"].sum():,}",
    "Total Desconto",
    col_dir,
)

base_status = base.groupby("Status", as_index=False).count()
base_status = base_status.rename(columns={"Código Projeto": "Quantidade"})
base_status = base_status.sort_values(by="Quantidade", ascending=False)


grafico = px.funnel(base_status, x="Quantidade", y="Status")
st.plotly_chart(grafico)
