from functools import lru_cache

from supabase import create_client

from app.core.settings import settings


@lru_cache
def get_admin_client():
    # Created once and reused, so routes can call this on every request cheaply
    return create_client(
        str(settings.supabase_url), str(settings.supabase_service_role_key)
    )
