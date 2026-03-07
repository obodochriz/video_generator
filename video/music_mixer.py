from moviepy import AudioFileClip, CompositeAudioClip


def mix_audio(narration_path, music_path, output_path):
    narration = AudioFileClip(narration_path)
    music = AudioFileClip(music_path).with_duration(narration.duration).volumex(0.2)

    final_audio = CompositeAudioClip([narration, music])
    final_audio.write_audiofile(output_path)