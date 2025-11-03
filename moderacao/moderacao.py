from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

cliente = OpenAI()

resposta = cliente.moderations.create(
    model="omni-moderation-2024-09-26", input="Insera um texto para textar a moderação."
)

moderacao = resposta.results[0]

print(moderacao.flagged)
print(moderacao.categories.to_dict())
