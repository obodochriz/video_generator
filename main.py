from ai_providers.openai_provider import OpenAIProvider
from ai_providers.gemini_provider import GeminiProvider
from video.scene_parser import parse_script
from video.image_generator import generate_image
from video.tts_generator import generate_voice
from video.subtitle_generator import generate_srt
from video.video_builder import build_video
from video.thumbnail_generator import generate_thumbnail
from video.utils import generate_filename_from_topic
from video.stock_video_fetcher import fetch_stock_video
import random


def main():

    topic = input("Topic: ")
    duration = int(input("Duration (seconds): "))
    model_choice = input("Model (openai/gemini): ").lower()

    if model_choice == "openai":
        provider = OpenAIProvider()
    else:
        provider = GeminiProvider()

    # 1️⃣ Generate script
    script_text = provider.generate_script(topic, duration)

    # 2️⃣ Parse JSON
    data = parse_script(script_text)
    scenes = data["scenes"]

    # 3️⃣ Generate scene assets
    STOCK_PROBABILITY = 0.6  # 60% stock, 40% AI
    generate_thumbnail(data["title"],model_choice)


    for i, scene in enumerate(scenes):

        generate_voice(scene["narration"], f"scene_{i}.mp3")

        video_path = f"scene_{i}.mp4"
        image_path = f"scene_{i}.png"

        stock_found = fetch_stock_video(
            scene["visual_prompt"],
            video_path
        )

        # -------------------------
        # Smart Random Blend Logic
        # -------------------------
        if stock_found and random.random() < STOCK_PROBABILITY:
            print(f"Scene {i}: Using STOCK")
            # Do nothing — stock will be used
        else:
            print(f"Scene {i}: Using AI")
            generate_image(
                scene["visual_prompt"],
                image_path,model_choice
            )

            # If stock was downloaded but we chose AI,
            # optionally delete stock file
            if stock_found:
                import os
                os.remove(video_path)

    # 4️⃣ Build video
    # build_video(scenes)
    # Generate filename from topic
    output_filename = generate_filename_from_topic(topic)

    # Build video
    build_video(scenes, output_filename)

    print(f"✅ Video generated: {output_filename}")

    # 5️⃣ Subtitles
    generate_srt(scenes, "subtitles.srt")

    # 6️⃣ Thumbnail
    # generate_thumbnail(data["title"],model_choice)

    print("✅ Video, subtitles, and thumbnail generated.")


if __name__ == "__main__":
    main()