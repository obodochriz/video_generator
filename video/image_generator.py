import base64
from config import settings


def generate_openai_image(prompt: str, output_path: str):
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1920x1080"
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    with open(output_path, "wb") as f:
        f.write(image_bytes)


def generate_gemini_image(prompt: str, output_path: str):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=settings.gemini_api_key)

    for model in client.models.list():
        if "imagen" in model.name.lower() or "image" in model.name.lower():
            print(model.name)

    response = client.models.generate_images(
        model="imagen-4.0-generate-001",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            aspect_ratio="16:9"
        )
    )

    image_bytes = response.generated_images[0].image.image_bytes

    with open(output_path, "wb") as f:
        f.write(image_bytes)


def generate_image(prompt: str, output_path: str, provider: str):

    if provider == "openai":
        print("🖼 Generating image with OpenAI...")
        generate_openai_image(prompt, output_path)

    elif provider == "gemini":
        print("🖼 Generating image with Gemini...")
        generate_gemini_image(prompt, output_path)

    else:
        raise ValueError("Invalid provider selected.")