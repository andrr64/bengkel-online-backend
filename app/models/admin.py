from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Enum   
from app.core.database import Base
from sqlalchemy.sql.expression import true
from app.models.role import Role

class AdminTable(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    aktif = Column(Boolean, nullable=False, server_default=true())
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    dibuat = Column(DateTime(timezone=True), server_default=func.now())
    role = Column(Enum(Role), default=Role.admin.value, nullable=False)
    diperbaharui = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())