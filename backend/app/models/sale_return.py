from datetime import date

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class SaleReturn(Base):
    __tablename__ = "sale_returns"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    return_no = Column(
        String(50),
        unique=True,
        nullable=False
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    return_date = Column(
        Date,
        default=date.today
    )

    total_amount = Column(
        Float,
        default=0
    )

    remarks = Column(
        String(255),
        nullable=True
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    customer = relationship("Customer")

    user = relationship("User")

    items = relationship(
        "SaleReturnItem",
        back_populates="sale_return",
        cascade="all, delete-orphan"
    )