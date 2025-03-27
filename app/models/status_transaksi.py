from app.core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class StatusTransaksiTable(Base):
    __tablename__ = "status_transaksi"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    dibuat = Column(DateTime(timezone=True), server_default=func.now())