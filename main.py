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
import glob
import os
import random
import shutil


def cleanup_scene_assets():
    patterns = ["scene_*.mp3", "scene_*.mp4", "scene_*.png"]
    for pattern in patterns:
        for path in glob.glob(pattern):
            try:
                os.remove(path)
                print(f"🧹 Deleted: {path}")
            except OSError as e:
                print(f"⚠ Could not delete {path}: {e}")


def main():

    topic = input("Topic: ")
    duration = int(input("Duration (seconds): "))
    model_choice = input("Model (openai/gemini): ").lower()
    if model_choice not in {"openai", "gemini"}:
        raise ValueError("Model must be either 'openai' or 'gemini'.")

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
                os.remove(video_path)

    # 3.5️⃣ Always append closing CTA segment
    cta_text = "Kindly like and subscribe to ensure you see future videos"
    cta_index = len(scenes)
    generate_voice(cta_text, f"scene_{cta_index}.mp3")

    # Reuse previous visual asset for continuity, if available.
    if cta_index > 0:
        prev_video = f"scene_{cta_index - 1}.mp4"
        prev_image = f"scene_{cta_index - 1}.png"
        cta_video = f"scene_{cta_index}.mp4"
        cta_image = f"scene_{cta_index}.png"

        if os.path.exists(prev_video):
            shutil.copy2(prev_video, cta_video)
        elif os.path.exists(prev_image):
            shutil.copy2(prev_image, cta_image)

    scenes.append({
        "narration": cta_text,
        "visual_prompt": "Closing call to action",
        "duration": 4
    })

    # 4️⃣ Build video
    # build_video(scenes)
    # Generate filename from topic
    output_filename = generate_filename_from_topic(topic)

    # Build video
    build_video(scenes, output_filename)

    print(f"✅ Video generated: {output_filename}")
    cleanup_scene_assets()

    # 5️⃣ Subtitles
    generate_srt(scenes, "subtitles.srt")

    # 6️⃣ Thumbnail
    # generate_thumbnail(data["title"],model_choice)

    print("✅ Video, subtitles, and thumbnail generated.")
    # Ensure clean up is well done 
    cleanup_scene_assets()

if __name__ == "__main__":
    main()
