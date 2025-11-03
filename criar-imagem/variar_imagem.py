import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

cliente = OpenAI()

with open("imagen.jpg", "rb") as arquivo_imagem:
    resposta = cliente.images.create_variation(
        model="gpt-image-1", n=3, image=arquivo_imagem
    )

imagens = resposta.data

for i, imagem in enumerate(imagens, start=1):
    url_imagem = imagem.url
    informacoes_imagem = requests.get(url_imagem)
    with open(f"imagem{i}.jpg", "wb") as arquivo_imagem:
        arquivo_imagem.write(informacoes_imagem.content)
