import requests
from config import settings


def fetch_stock_video(query: str, output_path: str) -> bool:
    headers = {
        "Authorization": settings.pexels_api_key
    }

    url = f"https://api.pexels.com/videos/search?query={query}&per_page=1"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        if not data.get("videos"):
            return False

        video_files = data["videos"][0]["video_files"]

        # Pick medium quality file
        video_url = sorted(video_files, key=lambda x: x["width"])[0]["link"]

        video_data = requests.get(video_url, timeout=20).content

        with open(output_path, "wb") as f:
            f.write(video_data)

        return True

    except Exception:
        return False