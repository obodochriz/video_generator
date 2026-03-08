import base64
from PIL import Image, ImageOps
from config import settings


def resize_image_to_1920x1080(image_path: str):
    with Image.open(image_path) as img:
        fitted = ImageOps.fit(
            img.convert("RGB"),
            (1920, 1080),
            method=Image.Resampling.LANCZOS
        )
        fitted.save(image_path, format="PNG")


def generate_openai_image(prompt: str, output_path: str):
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    image_bytes = None
    errors = []
    candidate_models = [settings.openai_image_model, "gpt-image-1", "dall-e-3"]

    for model_name in candidate_models:
        try:
            result = client.images.generate(
                model=model_name,
                prompt=prompt,
                size="1536x1024"
            )
            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)
            break
        except Exception as e:
            errors.append(f"{model_name}: {e}")

    if image_bytes is None:
        error_details = "; ".join(errors)
        raise RuntimeError(
            f"OpenAI image generation failed for all candidate models. {error_details}"
        )

    with open(output_path, "wb") as f:
        f.write(image_bytes)

    # OpenAI image sizes are limited; normalize output to exact 1920x1080.
    resize_image_to_1920x1080(output_path)


def generate_gemini_image(prompt: str, output_path: str):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=settings.gemini_api_key)

    #for model in client.models.list():
    #    if "imagen" in model.name.lower() or "image" in model.name.lower():
    #        print(model.name)

    response = client.models.generate_images(
        model=settings.gemini_image_model,
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
