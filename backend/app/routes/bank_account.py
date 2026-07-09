from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.roles import require_role
from app.database.connection import get_db

from app.models.bank_account import BankAccount
from app.models.user import User

from app.schemas.bank_account import (
    BankAccountCreate,
    BankAccountResponse,
)

from app.services.bank_account_service import (
    BankAccountService,
)


router = APIRouter(
    prefix="/bank-accounts",
    tags=["Bank Accounts"],
)


@router.post(
    "/",
    response_model=BankAccountResponse,
)
def create_bank_account(
    account: BankAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return BankAccountService.create(
        db=db,
        account=account,
        current_user=current_user,
    )


@router.get(
    "/",
    response_model=list[BankAccountResponse],
)
def get_bank_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return db.query(BankAccount).all()