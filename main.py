# Importar as bibliotecasa
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Criar as funções de carregamento de dados
# Cotações de do Itaú - ITUB4 - 2010 a 2024


@st.cache_data
def carregar_dados(empresas):
    dados = pd.DataFrame()
    for ticker in empresas:
        acao = yf.Ticker(ticker)
        cotacoes = acao.history(start="2023-09-01", end=datetime.today())
        if not cotacoes.empty:
            dados[ticker] = cotacoes["Close"]
    return dados


st.write(
    """
        # App Preço de Ações
        O gráfico abaixo representa a evolução do preço das ações ao longo dos anos"""
)

acoes = ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "ABEV3.SA", "GGBR4.SA"]

dados = carregar_dados(acoes)
lista_acoes = st.sidebar.multiselect("Escolha as ações para visualizar", dados.columns)

st.sidebar.header("Filtros")


#  Filtra as acoes
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})

# Filtra as datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
filtro_data = st.sidebar.slider("Selecione o período", min_value=data_inicial, max_value=data_final, value=(data_inicial, data_final), step=timedelta(days=1))

dados = dados.loc[filtro_data[0]:filtro_data[1]]

# # Cria o gráfico
st.line_chart(dados)
