from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Enum
from app.core.database import Base
from sqlalchemy.sql.expression import true
from app.models.role import Role

class MitraTable(Base):
    __tablename__ = "mitra"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    password = Column(String, nullable=False)
    no_telepon = Column(String, unique=True, nullable=False, index=True)
    dibuat = Column(DateTime(timezone=True), server_default=func.now())
    diperbaharui = Column(DateTime(timezone=True), onupdate=func.now())
    role = Column(Enum(Role), default=Role.mitra.value, nullable=False)
    aktif = Column(Boolean, nullable=False, server_default=true())