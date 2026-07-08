from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.auth.dependencies import get_current_user

from app.models.user import User

from app.schemas.ledger import CustomerLedgerResponse

from app.services.ledger_service import LedgerService


router = APIRouter(
    prefix="/ledger",
    tags=["Ledger"],
)


@router.get(
    "/customer/{customer_id}",
    response_model=CustomerLedgerResponse,
)
def customer_ledger(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return LedgerService.customer_ledger(
        db=db,
        customer_id=customer_id,
    )