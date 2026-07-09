from datetime import date, datetime

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


class BankTransaction(Base):
    __tablename__ = "bank_transactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    bank_account_id = Column(
        Integer,
        ForeignKey("bank_accounts.id"),
        nullable=False,
    )

    transaction_date = Column(
        Date,
        default=date.today,
        nullable=False,
    )

    transaction_type = Column(
        String(10),
        nullable=False,
    )  # CREDIT / DEBIT

    amount = Column(
        Float,
        nullable=False,
    )

    reference_no = Column(
        String(100),
        nullable=True,
    )

    remarks = Column(
        String(255),
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

    bank_account = relationship("BankAccount")
    user = relationship("User")