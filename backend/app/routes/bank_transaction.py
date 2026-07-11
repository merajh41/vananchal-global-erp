from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.roles import require_role
from app.database.connection import get_db

from app.models.bank_transaction import BankTransaction
from app.models.user import User

from app.schemas.bank_transaction import (
    BankTransactionCreate,
    BankTransactionResponse,
)

from app.services.bank_transaction_service import (
    BankTransactionService,
)


router = APIRouter(
    prefix="/bank-transactions",
    tags=["Bank Transactions"],
)


@router.post(
    "/",
    response_model=BankTransactionResponse,
)
def create_bank_transaction(
    transaction: BankTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return BankTransactionService.create(
        db=db,
        transaction=transaction,
        current_user=current_user,
    )


@router.get(
    "/",
    response_model=list[BankTransactionResponse],
)
def get_bank_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return db.query(BankTransaction).all()