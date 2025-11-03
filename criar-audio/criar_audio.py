import requests
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

cliente = OpenAI()


# Cria o áudio conforme pedido/prompt
def criar_audio_prompt():
    resposta = cliente.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"format": "wav", "voice": "allooy"},
        messages=[
            {
                "role": "user",
                "content": "Crie um áudio convidando as pessoas para aprender Python",
            }
        ],
    )

    faixa_audio = resposta.choices[0].message.audio.data
    return faixa_audio


# Cria áudio a partir de um texto
def criar_audio_texto(texto):
    resposta = cliente.audio.speech.create(
        model="tts-1", voice="alloy", response_format="wav", input=texto
    )
    return resposta


texto = "Se você quer aprender Python e não sabe por onde começar, venha comigo que lhe mostro o caminho."

faixa_audio_bytes = base64.b64decode(criar_audio_prompt())

with open("audio.wav", "wb") as arquivo_audio:
    arquivo_audio.write(faixa_audio_bytes)

criar_audio_texto(texto).write_to_file("audio-texto.wav")
