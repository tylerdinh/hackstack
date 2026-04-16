from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl
from pathlib import Path

from typing import Optional

env_path = Path(__file__).parent.parent.parent / ".env"

class Settings(BaseSettings):
    supabase_url: Optional[HttpUrl] = None
    supabase_anon_key: Optional[str] = None
    supabase_service_role_key: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=env_path,
    )

settings = Settings()