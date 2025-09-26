import streamlit as st
import pandas as pd

@st.cache_data
def carregar_dados():
    tabela = pd.read_excel("Base.xlsx")
    return tabela

base = carregar_dados()

st.title("Hash&Co")
st.write("Bem vindo, Erik")
st.table(base.head(10))