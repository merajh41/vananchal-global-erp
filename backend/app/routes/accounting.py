from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.roles import require_role
from app.database.connection import get_db

from app.models.user import User

from app.schemas.accounting import (
    ChartOfAccountCreate,
    ChartOfAccountResponse,
    VoucherCreate,
    VoucherResponse,
)

from app.services.account_seed_service import AccountSeedService
from app.services.accounting_service import AccountingService


router = APIRouter(
    prefix="/accounting",
    tags=["Accounting"],
)


# -----------------------------
# Chart of Accounts
# -----------------------------

@router.post(
    "/chart-of-accounts",
    response_model=ChartOfAccountResponse,
)
def create_chart_of_account(
    account: ChartOfAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return AccountingService.create_chart_of_account(
        db=db,
        account=account,
        current_user=current_user,
    )


@router.get(
    "/chart-of-accounts",
    response_model=list[ChartOfAccountResponse],
)
def get_chart_of_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return AccountingService.get_chart_of_accounts(db)


@router.post("/seed-chart-of-accounts")
def seed_chart_of_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    AccountSeedService.seed_default_accounts(
        db=db,
        created_by=current_user.id,
    )

    return {
        "message": "Default Chart of Accounts created successfully."
    }


# -----------------------------
# Voucher Engine
# -----------------------------

@router.post(
    "/vouchers",
    response_model=VoucherResponse,
)
def create_voucher(
    voucher: VoucherCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return AccountingService.create_voucher(
        db=db,
        voucher=voucher,
        current_user=current_user,
    )