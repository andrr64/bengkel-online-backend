from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base

class MerekTable(Base):
    __tablename__ = "merek"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False, unique=True)
    dibuat = Column(DateTime(timezone=True), server_default=func.now())
    diperbaharui = Column(DateTime(timezone=True), onupdate=func.now())