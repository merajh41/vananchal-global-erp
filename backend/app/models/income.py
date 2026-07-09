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


class Income(Base):
    __tablename__ = "incomes"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    income_date = Column(
        Date,
        default=date.today,
        nullable=False,
    )

    category = Column(
        String(100),
        nullable=False,
    )

    amount = Column(
        Float,
        nullable=False,
    )

    payment_mode = Column(
        String(30),
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

    user = relationship("User")