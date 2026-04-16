from supabase import create_client
from app.core.settings import settings

def get_admin_client():
    return create_client(str(settings.supabase_url), str(settings.supabase_service_role_key))