from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.roles import require_role
from app.database.connection import get_db

from app.models.user import User

from app.schemas.general_ledger import GeneralLedgerEntry
from app.services.general_ledger_service import GeneralLedgerService


router = APIRouter(
    prefix="/general-ledger",
    tags=["General Ledger"],
)


@router.get(
    "/",
    response_model=list[GeneralLedgerEntry],
)
def get_general_ledger(
    account: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return GeneralLedgerService.get_ledger(
        db=db,
        account=account,
    )