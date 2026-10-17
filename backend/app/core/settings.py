from pathlib import Path

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).parent.parent.parent / ".env"


class Settings(BaseSettings):
    # Required: startup fails with a clear "field required" error if these are missing from backend/.env
    supabase_url: HttpUrl
    supabase_service_role_key: str

    model_config = SettingsConfigDict(
        env_file=env_path,
        extra="ignore",  # don't crash on unrelated keys in .env
    )


settings = Settings()
