from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.admin import AdminTable
from app.core.security import hash_password

def daftar_admin(db: Session, username: str, password: str):
    existing_admin = db.query(AdminTable).filter(AdminTable.username == username).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Username sudah digunakan")
    
    hashed_password = hash_password(password)
    admin = AdminTable(
        username=username,
        password=hashed_password
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin
