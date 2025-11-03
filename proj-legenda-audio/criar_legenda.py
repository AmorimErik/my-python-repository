from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment


def criar_legenda(arquivo_video, contexto):
    extensao_arquivo = arquivo_video.name.split(".")[1]
    audio = AudioSegment.from_file(file=arquivo_video, format=extensao_arquivo)

    audio.export("audio.mp3", format="mp3")

    load_dotenv()

    cliente = OpenAI()

    with open("audio.mp3", "rb") as arquivo:
        transcricao = cliente.audio.transcriptions.create(
            file=arquivo,
            model="whisper-1",
            language="pt",
            response_format="srt",
            prompt=contexto,
        )

    with open("legenda.str", "w", encoding="utf-8") as arquivo_legenda:
        arquivo_legenda.write(transcricao)

    return transcricao
