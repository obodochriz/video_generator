def generate_srt(scenes, output_path):
    current_time = 0

    with open(output_path, "w", encoding="utf-8") as f:
        for i, scene in enumerate(scenes, 1):
            start = current_time
            end = current_time + scene["duration"]
            current_time = end

            f.write(f"{i}\n")
            f.write(f"{format_time(start)} --> {format_time(end)}\n")
            f.write(scene["narration"] + "\n\n")


def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hrs:02}:{mins:02}:{secs:02},000"