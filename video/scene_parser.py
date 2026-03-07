import json
import re


def parse_script(script_text: str):
    if not script_text:
        raise ValueError("AI returned empty response.")

    # Remove markdown code blocks if present
    cleaned = re.sub(r"```json|```", "", script_text).strip()

    # Extract first JSON object found
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)

    if not match:
        raise ValueError("No valid JSON object found in AI response.")

    json_str = match.group(0)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON returned by AI: {e}")