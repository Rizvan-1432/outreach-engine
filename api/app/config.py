from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Outreach Engine API"
    debug: bool = False
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    n8n_webhook_secret: str = ""
    enrichment_api_key: str = ""


settings = Settings()
