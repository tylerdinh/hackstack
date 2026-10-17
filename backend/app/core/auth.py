from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import AuthApiError

from app.storage.supabase_utils import get_admin_client

bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
):
    """Route dependency: verifies the Supabase access token sent by the frontend.

    Usage: `def my_route(user = Depends(get_current_user)): ...`
    """
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing bearer token")
    try:
        response = get_admin_client().auth.get_user(credentials.credentials)
    except AuthApiError:
        response = None
    if response is None or response.user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token")
    return response.user
