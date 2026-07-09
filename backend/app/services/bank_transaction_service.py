from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.bank_account import BankAccount
from app.models.bank_transaction import BankTransaction
from app.models.user import User

from app.schemas.bank_transaction import BankTransactionCreate


class BankTransactionService:

    @staticmethod
    def create(
        db: Session,
        transaction: BankTransactionCreate,
        current_user: User,
    ):

        account = (
            db.query(BankAccount)
            .filter(
                BankAccount.id == transaction.bank_account_id
            )
            .first()
        )

        if not account:
            raise HTTPException(
                status_code=404,
                detail="Bank account not found.",
            )

        transaction_type = transaction.transaction_type.upper()

        if transaction_type not in ("CREDIT", "DEBIT"):
            raise HTTPException(
                status_code=400,
                detail="Transaction type must be CREDIT or DEBIT.",
            )

        if transaction_type == "CREDIT":
            account.current_balance += transaction.amount
        else:
            if account.current_balance < transaction.amount:
                raise HTTPException(
                    status_code=400,
                    detail="Insufficient bank balance.",
                )

            account.current_balance -= transaction.amount

        db_transaction = BankTransaction(
            bank_account_id=transaction.bank_account_id,
            transaction_date=transaction.transaction_date,
            transaction_type=transaction_type,
            amount=transaction.amount,
            reference_no=transaction.reference_no,
            remarks=transaction.remarks,
            created_by=current_user.id,
        )

        db.add(db_transaction)

        db.commit()
        db.refresh(db_transaction)

        return db_transaction