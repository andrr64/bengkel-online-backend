from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.core.config import settings
from sqlalchemy.schema import DropTable

# Buat engine SQLAlchemy
engine = create_engine(settings.DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base untuk deklarasi model
Base = declarative_base()

def init_db():
    from app.models.pelanggan import PelangganTable
    from app.models.admin import AdminTable
    from app.models.mitra import MitraTable
    from app.models.kategori_produk import KategoriProdukTable
    from app.models.merek import MerekTable
    from app.models.status_transaksi import StatusTransaksiTable
    from app.models.transaksi_produk import TransaksiPembelianProdukTable
    from app.models.transaksi_booking import TransaksiBookingTable
    from app.models.produk import ProdukTable

    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Drop tables in the correct order
    tables_to_drop = reversed(metadata.sorted_tables)

    with engine.connect() as conn:
        for table in tables_to_drop:
            conn.execute(DropTable(table))
        conn.commit()  # Pastikan perubahan tersimpan

    # Buat ulang tabel
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        status_transaksi = [
            {'id': 1, 'nama': "Sedang diproses"},
            {'id': 2, 'nama': 'Sedang dikirim'},
            {'id': 5, 'nama': 'Selesai'},
            {'id': 6, 'nama': 'Dibatalkan'}
        ]

        list_merek = [
            {'nama': 'Honda'},
            {'nama': 'Suzuki'},
            {'nama': 'Yamaha'},
            {'nama': 'Kawasaki'}
        ]

        for merek in list_merek:
            db.add(MerekTable(**merek))
        for status in status_transaksi:
            db.add(StatusTransaksiTable(**status))

        db.commit()
    except Exception as e:
        db.rollback()
        print("Error:", e)
    finally:
        db.close()

# Dependency untuk mendapatkan session database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()