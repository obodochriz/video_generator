from google import genai
from config import settings
from ai_providers.base import AIProvider


class GeminiProvider(AIProvider):

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    def generate_script(self, topic: str, duration: int) -> str:
        prompt = f"""
        Create a YouTube video about {topic}.
        Duration: {duration} seconds.

        Return JSON:
        {{
          "title": "...",
          "scenes": [
            {{
              "narration": "...",
              "visual_prompt": "...",
              "duration": 5
            }}
          ]
        }}
        """

        response = self.client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        return response.text

