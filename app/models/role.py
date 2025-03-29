from enum import Enum as PyEnum
from sqlalchemy.dialects.postgresql import ENUM

class Role(PyEnum):
    pelanggan = "pelanggan"
    mitra = "mitra"
    admin = "admin"
    
role_enum = ENUM(*[role.value for role in Role], name="role_type", create_type=False)