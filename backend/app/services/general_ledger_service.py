from sqlalchemy.orm import Session

from app.models.journal_entry import JournalEntry


class GeneralLedgerService:

    @staticmethod
    def get_ledger(
        db: Session,
        account: str,
    ):

        entries = (
            db.query(JournalEntry)
            .filter(
                JournalEntry.account == account
            )
            .order_by(
                JournalEntry.entry_date,
                JournalEntry.id,
            )
            .all()
        )

        balance = 0
        ledger = []

        for entry in entries:

            balance += entry.debit
            balance -= entry.credit

            ledger.append({
                "date": entry.entry_date,
                "account": entry.account,
                "debit": entry.debit,
                "credit": entry.credit,
                "balance": balance,
                "narration": entry.narration,
                "reference_no": entry.reference_no,
            })

        return ledger