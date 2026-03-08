import requests
from config import settings

TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080


def fetch_stock_video(query: str, output_path: str) -> bool:
    headers = {
        "Authorization": settings.pexels_api_key
    }

    url = f"https://api.pexels.com/videos/search?query={query}&per_page=10"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("videos"):
            return False

        best_file = None
        best_score = -1
        for video in data["videos"]:
            for video_file in video.get("video_files", []):
                width = video_file.get("width")
                height = video_file.get("height")
                file_type = (video_file.get("file_type") or "").lower()
                if width != TARGET_WIDTH or height != TARGET_HEIGHT:
                    continue
                if "mp4" not in file_type:
                    continue

                score = video_file.get("fps") or 0
                if score > best_score:
                    best_score = score
                    best_file = video_file

        if best_file is None:
            return False

        video_url = best_file["link"]
        video_data = requests.get(video_url, timeout=20).content

        with open(output_path, "wb") as f:
            f.write(video_data)

        return True

    except Exception as e:
        print(f"Stock video fetch failed for '{query}': {e}")
        return False
