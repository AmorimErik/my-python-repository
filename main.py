import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from models import session, Usuario
from sair import sair

lista_usuarios = session.query(Usuario).all()

credenciais = {
    "usernames": {
        usuario.email: {"name": usuario.nome, "password": usuario.senha}
        for usuario in lista_usuarios
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


def logout():
    authenticator.logout()


# Autenticar Usuário
dados_usuario = autenticar_usuario(authenticator)

if dados_usuario:
    @st.cache_data
    def carregar_dados():
        tabela = pd.read_excel("Base.xlsx")
        return tabela

    base = carregar_dados()

    email_usuario = dados_usuario["username"]
    usuario = session.query(Usuario).filter_by(email=email_usuario).first()

    eh_admin = usuario.admin

    if eh_admin:
        pg = st.navigation(
            {
                "Home": [st.Page("homepage.py", title="Hash&Co")],
                "Dashboards": [
                    st.Page("dashboard.py", title="Dashboard"),
                    st.Page("indicadores.py", title="Indicadores"),
                ],
                "Conta": [
                    st.Page(logout, title="Sair"),
                    st.Page("criar_conta.py", title="Criar Conta"),
                ],
            }
        )
    else:
        pg = st.navigation(
            {
                "Home": [st.Page("homepage.py", title="Hash&Co")],
                "Dashboards": [
                    st.Page("dashboard.py", title="Dashboard"),
                    st.Page("indicadores.py", title="Indicadores"),
                ],
                "Conta": [
                    st.Page(logout, title="Sair"),
                ],
            }
        )

    pg.run()
