from sqlalchemy import Column, Integer, String

from app.database.base import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), unique=True, nullable=False)

    address = Column(String(255))

    manager = Column(String(100))