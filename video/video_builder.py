from moviepy.video.fx import FadeIn, FadeOut
import os
from moviepy import (
    VideoFileClip,
    ImageClip,
    ColorClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips
)
from moviepy.video.fx import Loop
#from moviepy.audio.fx import MultiplySpeed


# =========================
# YOUTUBE TARGET SETTINGS
# =========================
TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080
TARGET_SIZE = (TARGET_WIDTH, TARGET_HEIGHT)


# =========================
# FIT ANY CLIP TO 16:9
# =========================
def fit_to_youtube(clip):
    """
    Resize clip to 1920x1080 without distortion.
    If vertical, create blurred background.
    """

    # Resize by height first
    clip_resized = clip.resized(height=TARGET_HEIGHT)

    # If width too small → blurred background
    if clip_resized.w < TARGET_WIDTH:

        background = (
            clip.resized(width=TARGET_WIDTH)
            .cropped(
                x_center=clip.w / 2,
                y_center=clip.h / 2,
                width=TARGET_WIDTH,
                height=TARGET_HEIGHT
            )
            .with_opacity(0.4)
        )

        clip_resized = clip_resized.with_position("center")

        return CompositeVideoClip(
            [background, clip_resized],
            size=TARGET_SIZE
        )

    # Otherwise center crop to 1920x1080
    return clip_resized.cropped(
        x_center=clip_resized.w / 2,
        y_center=clip_resized.h / 2,
        width=TARGET_WIDTH,
        height=TARGET_HEIGHT
    )


# =========================
# MAIN VIDEO BUILDER
# =========================
def build_video(scenes, output_filename: str):

    clips = []

    for i, scene in enumerate(scenes):

        audio_path = f"scene_{i}.mp3"
        video_path = f"scene_{i}.mp4"
        image_path = f"scene_{i}.png"

        # Increase narration speed to 1.25x
        audio = AudioFileClip(audio_path)
        # Increase narration speed
        audio = audio.with_speed_scaled(1.25)

        # -------------------------
        # STOCK VIDEO CASE
        # -------------------------
        if os.path.exists(video_path):

            video_clip = VideoFileClip(video_path)

            # Trim or loop
            if video_clip.duration > audio.duration:
                video_clip = video_clip.subclipped(0, audio.duration)
            else:
                video_clip = video_clip.with_effects([
                    Loop(duration=audio.duration)
                ])

            video_clip = fit_to_youtube(video_clip)

            clip = video_clip.with_audio(audio)

        # -------------------------
        # IMAGE FALLBACK CASE
        # -------------------------
        elif os.path.exists(image_path):

            # Fit first, then animate so every frame remains 1920x1080-compatible.
            duration = max(audio.duration, 0.01)
            base_img = fit_to_youtube(
                ImageClip(image_path).with_duration(duration)
            )
            moving_img = (
                base_img
                .resized(lambda t: 1.0 + (0.12 * (t / duration)))
                .with_position("center")
            )
            motion_canvas = CompositeVideoClip(
                [moving_img],
                size=TARGET_SIZE
            ).with_duration(duration)
            clip = motion_canvas.with_audio(audio)

        # -------------------------
        # EMERGENCY FALLBACK
        # -------------------------
        else:
            print(f"⚠ No visual found for scene {i}")

            blank = ColorClip(
                size=TARGET_SIZE,
                color=(0, 0, 0)
            ).with_duration(audio.duration)

            clip = blank.with_audio(audio)

        clips.append(clip)

    # -------------------------
    # CONCATENATE
    # -------------------------
    final = concatenate_videoclips(clips, method="compose")

    # -------------------------
    # EXPORT
    # -------------------------
    final.write_videofile(
        output_filename,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        bitrate="10000k"
    )
