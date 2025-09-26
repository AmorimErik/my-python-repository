import streamlit as st


def sair(authenticator):
    st.title("Sair da Conta")
    authenticator.logout("Clique aqui para sair", "sidebar")
