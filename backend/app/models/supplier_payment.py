from datetime import datetime, date

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Date,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class SupplierPayment(Base):
    __tablename__ = "supplier_payments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id"),
        nullable=False
    )

    payment_date = Column(
        Date,
        default=date.today
    )

    amount = Column(
        Float,
        nullable=False
    )

    payment_mode = Column(
        String(30),
        nullable=False
    )

    reference_no = Column(
        String(100),
        nullable=True
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

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    supplier = relationship("Supplier")

    user = relationship("User")