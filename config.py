from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    gemini_api_key: str
    pexels_api_key: str
    openai_script_model: str = "gpt-4o-mini"
    openai_image_model: str = "gpt-image-1"
    gemini_script_model: str = "gemini-3-pro-preview"
    gemini_image_model: str = "imagen-4.0-generate-001"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()
