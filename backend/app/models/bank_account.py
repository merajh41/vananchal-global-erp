from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    bank_name = Column(
        String(150),
        nullable=False,
    )

    account_name = Column(
        String(150),
        nullable=False,
    )

    account_number = Column(
        String(100),
        nullable=False,
        unique=True,
    )

    ifsc_code = Column(
        String(20),
        nullable=False,
    )

    opening_balance = Column(
        Float,
        default=0,
        nullable=False,
    )

    current_balance = Column(
        Float,
        default=0,
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

    user = relationship("User")