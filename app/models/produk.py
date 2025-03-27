from sqlalchemy import Column, Integer, String, ForeignKey, Double, DateTime, func
from app.core.database import Base

class ProdukTable(Base):
    __tablename__ = "produk"
    
    id = Column(Integer, primary_key=True, index=True)
    id_merek = Column(Integer, ForeignKey('merek.id', ondelete='CASCADE'))
    id_kategori = Column(Integer, ForeignKey('kategori_produk.id', ondelete='CASCADE'))
    nama = Column(String)
    deskripsi = Column(String)
    harga = Column(Double)
    stok = Column(Integer, default=0)
    dibuat = Column(DateTime(timezone=True), server_default=func.now())
    diperbaharui = Column(DateTime(timezone=True), onupdate=func.now())