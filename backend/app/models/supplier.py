from sqlalchemy import Column, Integer, String

from app.database.base import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    contact_person = Column(String(100), nullable=True)

    phone = Column(String(20), nullable=True)

    email = Column(String(150), nullable=True)

    address = Column(String(255), nullable=True)

    gst_number = Column(String(50), nullable=True)