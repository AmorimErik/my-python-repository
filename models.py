from sqlalchemy import Boolean, Column, create_engine, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

db = create_engine("sqlite:///database/app.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    senha = Column("senha", String)
    email = Column("email", String)
    admin = Column("admin", Boolean)

    def __init__(self, nome, senha, email, admin=False):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.admin = admin


Base.metadata.create_all(bind=db)
