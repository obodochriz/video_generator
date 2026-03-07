import re


def generate_filename_from_topic(topic: str) -> str:
    # Lowercase
    name = topic.lower()

    # Replace spaces with underscore
    name = name.replace(" ", "_")

    # Remove non-alphanumeric characters except underscore
    name = re.sub(r"[^a-z0-9_]", "", name)

    return f"{name}.mp4"