# Importar as bibliotecasa
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Criar as funções de carregamento de dados
@st.cache_data
def carregar_dados(empresas):
    dados = pd.DataFrame()
    for ticker in empresas:
        acao = yf.Ticker(ticker)
        cotacoes = acao.history(start="2023-09-01", end=datetime.today())
        if not cotacoes.empty:
            dados[ticker] = cotacoes["Close"]
    return dados


@st.cache_data
def carregar_tickers_acoes():
    base_tickers = pd.read_csv("IBOV.csv", sep=";")
    tickers = list(base_tickers["Código"])
    tickers = [item + ".SA" for item in tickers]
    return tickers


acoes = carregar_tickers_acoes()
dados = carregar_dados(acoes)

# Cria a interface do Streamlit
st.write(
    """
        # App Preço de Ações
        O gráfico abaixo representa a evolução do preço das ações no período"""
)
# Barra lateral com o filtro
st.sidebar.header("Filtros")

lista_acoes = st.sidebar.multiselect("Escolha as ações para visualizar", dados.columns)

if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})

# Filtro datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
periodo = st.sidebar.slider(
    "Selecione o período para visualização",
    min_value=data_inicial,
    max_value=data_final,
    value=(data_inicial, data_final),
    step=timedelta(days=1),
)

dados = dados.loc[periodo[0] : periodo[1]]

# Cria o gráfico
st.line_chart(dados)

msg_performance = ""

if len(lista_acoes) == 0:
    lista_acoes = list(dados.columns)
elif len(lista_acoes) == 1:
    dados = dados.rename(columns={"Close": acao_unica})

carteira = [1000 for acao in lista_acoes]
saldo_inicial = sum(carteira)

for i, acao in enumerate(lista_acoes):
    performance = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1
    performance = float(performance)

    carteira[i] = carteira[i] * (performance + 1)

    # Colando cor texto
    if performance > 0:
        msg_performance = msg_performance + f"  \n{acao}: :green[{performance:.1%}]"
    elif performance < 0:
        msg_performance = msg_performance + f"  \n{acao}: :red[{performance:.1%}]"
    else:
        msg_performance = msg_performance + f"  \n{acao}: {performance:.1%}"

saldo_final = sum(carteira)
perf_carteira = saldo_final / saldo_inicial - 1

if perf_carteira > 0:
    msg_perf_carteira = (
        f"Performance da carteira com todos os ativos: :green[{perf_carteira:.1%}]"
    )
elif perf_carteira < 0:
    msg_perf_carteira = (
        f"Performance da carteira com todos os ativos: :red[{perf_carteira:.1%}]"
    )
else:
    msg_perf_carteira = (
        f"Performance da carteira com todos os ativos: {perf_carteira:.1%}"
    )

st.write(
    f"""
        ### Performance dos Ativos
        Essa foi a performance de cada ativo no período selecionado:
        {msg_performance}
        \n{msg_perf_carteira}
        """
)
