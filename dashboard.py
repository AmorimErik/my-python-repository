import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data_loader import carregar_dados

base = carregar_dados()

col_esq, col_meio, col_dir = st.columns([1, 1, 1])

setor = col_esq.selectbox("Setor", list(base["Setor"].unique()))
status = col_meio.selectbox("Status", list(base["Status"].unique()))

base = base[(base["Setor"] == setor) & (base["Status"] == status)]
base_mensal = (
    base.groupby(base["Data Chegada"].dt.to_period("M"))
    .sum(numeric_only=True)
    .reset_index()
)
base_mensal["Data Chegada"] = base_mensal["Data Chegada"].dt.to_timestamp()

container = st.container(border=True)
with container:
    st.write("### Total de Projetos por mês (R$)")
    grafico_area = px.area(base_mensal, x="Data Chegada", y="Valor Negociado")
    st.plotly_chart(grafico_area)

    col_esq, col_dir = st.columns([3, 1.5])
    col_esq.write("### Comparação Orçado x Pago")
    base_mensal["Ano"] = base_mensal["Data Chegada"].dt.year
    anos = list(base_mensal["Ano"].unique())
    ano_selecionado = col_dir.selectbox("Ano", anos)

    base_mensal = base_mensal[base_mensal["Ano"] == ano_selecionado]
    total_pago = base_mensal["Valor Negociado"].sum()
    total_desconto = base_mensal["Desconto Concedido"].sum()

    col_esq, col_dir = st.columns([1, 1])
    col_esq.metric("Total Pago", f"R$ {total_pago:,}")
    col_dir.metric("Total Desconto", f"R$ {total_desconto:,}")

    grafico_barra = go.Figure(
        data=[
            go.Bar(
                name="Valor Orçado",
                x=base_mensal["Data Chegada"],
                y=base_mensal["Valor Orçado"],
                text=base_mensal["Valor Orçado"],
            ),
            go.Bar(
                name="Valor Pago",
                x=base_mensal["Data Chegada"],
                y=base_mensal["Valor Negociado"],
                text=base_mensal["Valor Negociado"],
            ),
        ]
    )
    grafico_barra.update_layout(barmode="group")
    st.plotly_chart(grafico_barra)

st.table(base_mensal.head(15))
