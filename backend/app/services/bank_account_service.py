from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.bank_account import BankAccount
from app.models.user import User

from app.schemas.bank_account import BankAccountCreate


class BankAccountService:

    @staticmethod
    def create(
        db: Session,
        account: BankAccountCreate,
        current_user: User,
    ):

        exists = (
            db.query(BankAccount)
            .filter(
                BankAccount.account_number == account.account_number
            )
            .first()
        )

        if exists:
            raise HTTPException(
                status_code=400,
                detail="Bank account already exists.",
            )

        db_account = BankAccount(
            bank_name=account.bank_name,
            account_name=account.account_name,
            account_number=account.account_number,
            ifsc_code=account.ifsc_code,
            opening_balance=account.opening_balance,
            current_balance=account.opening_balance,
            created_by=current_user.id,
        )

        db.add(db_account)
        db.commit()
        db.refresh(db_account)

        return db_account