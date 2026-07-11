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


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    entry_date = Column(
        Date,
        default=date.today,
        nullable=False,
    )

    account = Column(
        String(100),
        nullable=False,
    )

    debit = Column(
        Float,
        default=0,
        nullable=False,
    )

    credit = Column(
        Float,
        default=0,
        nullable=False,
    )

    narration = Column(
        String(255),
        nullable=True,
    )

    reference_no = Column(
        String(100),
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