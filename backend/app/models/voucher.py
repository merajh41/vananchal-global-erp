from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class Voucher(Base):
    __tablename__ = "vouchers"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    voucher_no = Column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    voucher_date = Column(
        Date,
        nullable=False,
    )

    voucher_type = Column(
        String(20),
        nullable=False,
        index=True,
    )

    narration = Column(
        Text,
        nullable=True,
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    lines = relationship(
        "VoucherLine",
        back_populates="voucher",
        cascade="all, delete-orphan",
    )