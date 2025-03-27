from app.core.database import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, func, String

class TransaksiPembelianProdukTable(Base):
    __tablename__ = "transaksi_produk"
    id = Column(Integer, primary_key=True, index=True)
    id_pelanggan = Column(Integer, ForeignKey("pelanggan.id"), nullable=False)    
    id_mitra = Column(Integer, ForeignKey("mitra.id"), nullable=True)
    deskripsi = Column(String, nullable=True)
    status = Column(Integer, ForeignKey('status_transaksi.id'), nullable=False)
    dibuat = Column(DateTime(timezone=True), server_default=func.now())
    diperbaharui = Column(DateTime(timezone=True), onupdate=func.now())