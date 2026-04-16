from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl

from typing import Optional

class Settings(BaseSettings):
    supabase_url: Optional[HttpUrl] = None
    supabase_anon_key: Optional[str] = None
    supabase_service_role_key: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
    )

settings = Settings()