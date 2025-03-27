from app.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func

class TransaksiBookingTable(Base):
    __tablename__ = "transaksi_booking"
    
    id = Column(Integer, primary_key=True, index=True)
    id_mitra = Column(Integer, ForeignKey("mitra.id"), nullable=True)
    id_pelanggan = Column(Integer, ForeignKey("pelanggan.id"), nullable=True)
    nomor_urutan = Column(Integer, nullable=True)
    tanggal = Column(DateTime, nullable=False)
    deskripsi = Column(String, nullable=True)
    dibuat = Column(DateTime(timezone=True), server_default=func.now())
    diperbaharui = Column(DateTime(timezone=True), onupdate=func.now())