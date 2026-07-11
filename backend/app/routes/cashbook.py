from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.roles import require_role
from app.database.connection import get_db

from app.models.user import User

from app.schemas.cashbook import CashBookEntry
from app.services.cashbook_service import CashBookService


router = APIRouter(
    prefix="/cashbook",
    tags=["Cash Book"],
)


@router.get(
    "/",
    response_model=list[CashBookEntry],
)
def get_cashbook(
    from_date: date,
    to_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return CashBookService.get_cashbook(
        db=db,
        from_date=from_date,
        to_date=to_date,
    )