from datetime import timedelta

import httpx
from django.utils import timezone

from bus_service.settings import TDX_CLIENT_ID, TDX_CLIENT_SECRET

_current_value = None
_last_created_at = None


def get():
    if _is_expired():
        _create()
    return _current_value


def _is_expired():
    if _current_value is None or _last_created_at is None:
        return True
    if timezone.now() - _last_created_at > timedelta(days=1):
        return True
    return False


TDX_AUTH_URL = (
    "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
)


# Create an access token, should be used every day
def _create():
    global _current_value
    global _last_created_at

    r = httpx.post(
        TDX_AUTH_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": TDX_CLIENT_ID,
            "client_secret": TDX_CLIENT_SECRET,
        },
    )
    if r.status_code == 200:
        _current_value = r.json()["access_token"]
        _last_created_at = timezone.now()
    else:
        raise Exception(f"Unable to create access token from TDX: {r.text}")
