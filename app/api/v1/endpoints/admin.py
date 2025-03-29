from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.api.v1.schemas.admin import AdminCreate, AdminLogin
from app.services.admin.login import login_admin
from app.services.admin.register import daftar_admin
from app.core.security import create_access_token, create_refresh_token
from datetime import timedelta
from app.core.config import settings
from app.middleware.auth.admin import admin_auth_middleware

router = APIRouter()

@router.post("/admin/protected/register", dependencies=[Depends(admin_auth_middleware)])
def register(
    admin: AdminCreate,
    db: Session = Depends(get_db),
):
    admin = daftar_admin(db=db, username=admin.username, password=admin.password)
    if not admin:
        raise HTTPException(status_code=400, detail="Failed to register admin")
    return {"detail": "Admin registered"}

@router.post("/admin/login")
def login(response: Response,
          request: Request,
          data: AdminLogin, 
          db: Session = Depends(get_db)):
    admin = login_admin(db, data.username, data.password)
    if not admin:
        raise HTTPException(status_code=401, detail="Username atau Password salah!")
    
    access_token = create_access_token(
        {"sub": admin.username, "admin_id": str(admin.id)},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        {"sub": admin.username, "admin_id": str(admin.id)}
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )
    return {"detail": "Login berhasil"}