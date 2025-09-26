import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from sair import sair

senhas_criptografadas = stauth.Hasher(["******", "********", "*******"]).generate()
credenciais = {
    "usernames": {
        "email1@email.com": {"name": "jose", "password": senhas_criptografadas[0]},
        "email2@email.com": {"name": "joao", "password": senhas_criptografadas[1]},
        "email3@email.com": {"name": "mateus", "password": senhas_criptografadas[2]},
    }
}

authenticator = stauth.Authenticate(
    credenciais, "credenciais_hashco", "a$GbKG~5EO75", cookie_expiry_days=30
)


def autenticar_usuario(authenticator):
    nome, status_autenticacao, username = authenticator.login()
    if status_autenticacao:
        return {"nome": nome, "username": username}
    elif status_autenticacao == False:
        st.error("Combinação de usuário e senha inválidas")
    else:
        st.error("Preencha o formulário para fazer login.")


# Autenticar Usuário
dados_usuario = autenticar_usuario(authenticator)

if dados_usuario:

    @st.cache_data
    def carregar_dados():
        tabela = pd.read_excel("Base.xlsx")
        return tabela

    base = carregar_dados()

    pg = st.navigation(
        {
            "Home": [st.Page("homepage.py", title="Hash&Co")],
            "Dashboards": [
                st.Page("dashboard.py", title="Dashboard"),
                st.Page("indicadores.py", title="Indicadores"),
            ],
            "Conta": [
                st.Page("criar_conta.py", title="Criar conta"),
                st.Page(lambda: sair(authenticator), title="Sair"),
            ],
        }
    )

    pg.run()
