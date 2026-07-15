from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class ChartOfAccount(Base):
    __tablename__ = "chart_of_accounts"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    account_code = Column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    account_name = Column(
        String(150),
        nullable=False,
    )

    account_type = Column(
        String(30),
        nullable=False,
        index=True,
    )

    account_group = Column(
        String(50),
        nullable=False,
        index=True,
    )

    parent_id = Column(
        Integer,
        ForeignKey("chart_of_accounts.id"),
        nullable=True,
    )

    opening_balance = Column(
        Float,
        default=0,
        nullable=False,
    )

    balance_type = Column(
        String(10),
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
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

    parent = relationship(
        "ChartOfAccount",
        remote_side=[id],
    ) 
    voucher_lines = relationship(
    "VoucherLine",
    back_populates="account",
)

    user = relationship("User")