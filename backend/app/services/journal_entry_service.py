from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.journal_entry import JournalEntry
from app.models.user import User

from app.schemas.journal_entry import JournalEntryCreate


class JournalEntryService:

    @staticmethod
    def create(
        db: Session,
        journal: JournalEntryCreate,
        current_user: User,
    ):

        if journal.debit < 0 or journal.credit < 0:
            raise HTTPException(
                status_code=400,
                detail="Debit and Credit cannot be negative.",
            )

        if journal.debit == 0 and journal.credit == 0:
            raise HTTPException(
                status_code=400,
                detail="Either Debit or Credit must be greater than zero.",
            )

        if journal.debit > 0 and journal.credit > 0:
            raise HTTPException(
                status_code=400,
                detail="A journal entry cannot have both Debit and Credit values.",
            )

        db_entry = JournalEntry(
            entry_date=journal.entry_date,
            account=journal.account,
            debit=journal.debit,
            credit=journal.credit,
            narration=journal.narration,
            reference_no=journal.reference_no,
            created_by=current_user.id,
        )

        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)

        return db_entry

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(JournalEntry)
            .order_by(
                JournalEntry.entry_date.desc(),
                JournalEntry.id.desc(),
            )
            .all()
        )