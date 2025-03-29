from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.schema import CreateTable
from app.core.config import settings
from typing import List, Type
import logging
from sqlalchemy import event, DDL

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Buat engine SQLAlchemy
engine = create_engine(settings.DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base untuk deklarasi model
Base = declarative_base()

def get_all_models() -> List[Type[any]]:
    """Mengembalikan daftar semua model SQLAlchemy dalam aplikasi"""
    from app.models.pelanggan import PelangganTable
    from app.models.admin import AdminTable
    from app.models.mitra import MitraTable
    from app.models.kategori_produk import KategoriProdukTable
    from app.models.merek import MerekTable
    from app.models.status_transaksi import StatusTransaksiTable
    from app.models.transaksi_produk import TransaksiPembelianProdukTable
    from app.models.transaksi_booking import TransaksiBookingTable
    from app.models.produk import ProdukTable
    
    return [
        PelangganTable,
        AdminTable,
        MitraTable,
        KategoriProdukTable,
        MerekTable,
        StatusTransaksiTable,
        TransaksiPembelianProdukTable,
        TransaksiBookingTable,
        ProdukTable
    ]

def check_and_create_tables():
    """Memeriksa dan membuat tabel yang belum ada"""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    models = get_all_models()
    
    with engine.begin() as conn:
        for model in models:
            table_name = model.__tablename__
            if table_name not in existing_tables:
                logger.info(f"Membuat tabel: {table_name}")
                conn.execute(CreateTable(model.__table__))
            else:
                logger.info(f"Tabel {table_name} sudah ada")

def seed_initial_data():
    """Menambahkan data awal ke database"""
    db = SessionLocal()
    try:
        # Cek apakah data sudah ada
        if not db.query(MerekTable).first():
            list_merek = [
                {'nama': 'Honda'},
                {'nama': 'Suzuki'},
                {'nama': 'Yamaha'},
                {'nama': 'Kawasaki'}
            ]
            for merek in list_merek:
                db.add(MerekTable(**merek))
        
        if not db.query(StatusTransaksiTable).first():
            status_transaksi = [
                {'id': 1, 'nama': "Sedang diproses"},
                {'id': 2, 'nama': 'Sedang dikirim'},
                {'id': 5, 'nama': 'Selesai'},
                {'id': 6, 'nama': 'Dibatalkan'}
            ]
            for status in status_transaksi:
                db.add(StatusTransaksiTable(**status))
        
        db.commit()
        logger.info("Data awal berhasil ditambahkan")
    except Exception as e:
        db.rollback()
        logger.error(f"Gagal menambahkan data awal: {e}")
    finally:
        db.close()

def init_db():
    """Fungsi utama untuk inisialisasi database"""
    logger.info("Memulai inisialisasi database...")
    from app.models.role import Role
    try:
        # 1. Buat enum type jika belum ada
        with engine.connect() as conn:
            role_values = [role.value for role in Role]
            
            if not conn.dialect.has_type(conn, "role"):
                conn.execute(DDL(f"CREATE TYPE role AS ENUM ({', '.join(f'{role}' for role in role_values)})"))
                conn.commit()
            else:
                logger.info("Enum type 'role' sudah ada")
        check_and_create_tables()
        
        # Tambahkan data awal
        seed_initial_data()
        
        logger.info("Inisialisasi database selesai")
    except Exception as e:
        logger.error(f"Error selama inisialisasi database: {e}")
        raise

# Dependency untuk mendapatkan session database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()