from openai import OpenAI
from config import settings


def generate_voice(text: str, output_path: str):
    client = OpenAI(api_key=settings.openai_api_key)

    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    with open(output_path, "wb") as f:
        f.write(speech.content)