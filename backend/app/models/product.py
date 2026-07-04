from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), unique=True, nullable=False)

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    unit = Column(String(50), nullable=False)

    purchase_price = Column(Float, default=0)

    selling_price = Column(Float, default=0)

    opening_stock = Column(Float, default=0)

    category = relationship(
    "Category",
    back_populates="products"
)