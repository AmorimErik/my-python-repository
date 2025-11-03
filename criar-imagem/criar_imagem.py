import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

cliente = OpenAI()

resposta = cliente.images.generate(
    model="gpt-image-1",
    prompt="Uma imagem realista de um rato vestido com roupa indiana tocando trompete nos Alpes Suíços.",
    size="1024x1024",
    quality="auto",
)

url_imagem = resposta.data[0].url
print("Imagem gerada com sucesso!")
print(f"Link: {url_imagem}")

informacoes_imagem = requests.get(url_imagem)

with open("imagem.jpg", "wb") as arquivo_imagem:
    arquivo_imagem.write(informacoes_imagem.content)
