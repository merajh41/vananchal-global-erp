from sqlalchemy import Column, Integer, String
from app.database.base import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), nullable=False)

    owner = Column(String(100))

    gst = Column(String(20))

    phone = Column(String(20))

    email = Column(String(100))

    address = Column(String(300))