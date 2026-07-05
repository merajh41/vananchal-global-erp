from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class PurchaseReturnItem(Base):
    __tablename__ = "purchase_return_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    purchase_return_id = Column(
        Integer,
        ForeignKey("purchase_returns.id"),
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

    purchase_return = relationship(
        "PurchaseReturn",
        back_populates="items"
    )

    product = relationship("Product")

    warehouse = relationship("Warehouse")