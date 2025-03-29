from fastapi import Request, Response, HTTPException
from jose import JWTError, jwt
from datetime import timedelta
from app.core.config import settings
from app.core.security import create_access_token

def verify_token(token: str, expected_type: str = "access"):
    """Verifikasi token JWT dan kembalikan payload jika valid."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRETKEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != expected_type:
            return None
        return payload
    except JWTError:
        return None

def get_admin_id_from_access_token(access_token: str):
    """Coba ambil admin_id dari access token jika valid."""
    payload = verify_token(access_token, "access")
    return payload["admin_id"] if payload else None

def refresh_access_token_if_needed(refresh_token: str, response: Response):
    """Jika refresh token valid, buat access token baru."""
    refresh_payload = verify_token(refresh_token, "refresh")
    if refresh_payload:
        new_access_token = create_access_token(
            {"sub": refresh_payload["sub"], "admin_id": refresh_payload["admin_id"]},
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=False,
            samesite="strict",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        return refresh_payload["admin_id"]
    return None

def clear_auth_cookies(response: Response):
    """Hapus access token dan refresh token dari cookie."""
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

async def admin_auth_middleware(request: Request, response: Response):
    """Middleware untuk melindungi route admin."""
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    admin_id = get_admin_id_from_access_token(access_token)
    if admin_id:
        request.state.admin_id = admin_id
        return  # Valid, lanjut ke route

    # Coba refresh token jika access token tidak valid
    admin_id = refresh_access_token_if_needed(refresh_token, response)
    if admin_id:
        request.state.admin_id = admin_id
        return  # Valid, lanjut ke route

    # Jika kedua token tidak valid
    clear_auth_cookies(response)
    raise HTTPException(status_code=401, detail="Unauthorized")
