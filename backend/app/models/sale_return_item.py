from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class SaleReturnItem(Base):
    __tablename__ = "sale_return_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    sale_return_id = Column(
        Integer,
        ForeignKey("sale_returns.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    warehouse_id = Column(
        Integer,
        ForeignKey("warehouses.id"),
        nullable=False
    )

    quantity = Column(
        Float,
        nullable=False
    )

    rate = Column(
        Float,
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    sale_return = relationship(
        "SaleReturn",
        back_populates="items"
    )

    product = relationship("Product")

    warehouse = relationship("Warehouse")