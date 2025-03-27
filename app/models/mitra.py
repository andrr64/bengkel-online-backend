from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from app.core.database import Base
from sqlalchemy.sql.expression import true

class MitraTable(Base):
    __tablename__ = "mitra"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    password = Column(String, nullable=False)
    no_telepon = Column(String, unique=True, nullable=False, index=True)
    dibuat = Column(DateTime(timezone=True), server_default=func.now())
    diperbaharui = Column(DateTime(timezone=True), onupdate=func.now())
    aktif = Column(Boolean, nullable=False, server_default=true())