from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user
from app.auth.roles import require_role

from app.models.user import User
from app.models.purchase_return import PurchaseReturn

from app.schemas.purchase_return import (
    PurchaseReturnCreate,
    PurchaseReturnResponse,
)

from app.services.purchase_return_service import PurchaseReturnService

router = APIRouter(
    prefix="/purchase-returns",
    tags=["Purchase Returns"],
)


@router.post("/", response_model=PurchaseReturnResponse)
def create_purchase_return(
    purchase_return: PurchaseReturnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return PurchaseReturnService.create_purchase_return(
        db=db,
        purchase_return=purchase_return,
        current_user=current_user,
    )


@router.get("/", response_model=list[PurchaseReturnResponse])
def get_purchase_returns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(PurchaseReturn).all()