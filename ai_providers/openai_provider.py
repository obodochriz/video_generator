from openai import OpenAI
from config import settings
from ai_providers.base import AIProvider


class OpenAIProvider(AIProvider):

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

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

        response = self.client.chat.completions.create(
            model=settings.openai_script_model,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content
