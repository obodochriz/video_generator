from video.image_generator import generate_image


def generate_thumbnail(title: str, model_choice: str):
    prompt = f"Cinematic YouTube thumbnail, bold title text: {title}"
    print("🖼 Generating video Thumbnail...")
    generate_image(prompt, "thumbnail.png", model_choice)