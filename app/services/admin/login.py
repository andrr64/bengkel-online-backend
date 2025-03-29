from sqlalchemy.orm import Session
from app.models.admin import AdminTable
from app.core.security import hash_password, verify_password

def login_admin(db: Session, username: str, password: str):
    admin = db.query(AdminTable).filter(AdminTable.username == username).first()
    if not admin:
        return None
    if not verify_password(password, admin.password):
        return None
    return admin