from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class VoucherLine(Base):
    __tablename__ = "voucher_lines"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    voucher_id = Column(
        Integer,
        ForeignKey("vouchers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    account_id = Column(
        Integer,
        ForeignKey("chart_of_accounts.id"),
        nullable=False,
        index=True,
    )

    debit = Column(
        Numeric(18, 2),
        default=0,
        nullable=False,
    )

    credit = Column(
        Numeric(18, 2),
        default=0,
        nullable=False,
    )

    remarks = Column(
        String(255),
        nullable=True,
    )

    voucher = relationship(
        "Voucher",
        back_populates="lines",
    )

    account = relationship(
    "ChartOfAccount",
    back_populates="voucher_lines",
)
    