from sqlalchemy import Column, Integer, String

from app.database.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(150),
        nullable=False
    )

    mobile = Column(
        String(20),
        nullable=True
    )

    email = Column(
        String(150),
        nullable=True
    )

    address = Column(
        String(255),
        nullable=True
    )

    gst_number = Column(
        String(50),
        nullable=True
    )