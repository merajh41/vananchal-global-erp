from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.auth.dependencies import get_current_user
from app.auth.roles import require_role

from app.models.customer_receipt import CustomerReceipt
from app.models.user import User

from app.schemas.customer_receipt import (
    CustomerReceiptCreate,
    CustomerReceiptResponse,
)

from app.services.customer_receipt_service import CustomerReceiptService


router = APIRouter(
    prefix="/customer-receipts",
    tags=["Customer Receipts"],
)


@router.post("/", response_model=CustomerReceiptResponse)
def create_customer_receipt(
    receipt: CustomerReceiptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return CustomerReceiptService.create_receipt(
        db=db,
        receipt=receipt,
        current_user=current_user,
    )


@router.get("/", response_model=list[CustomerReceiptResponse])
def get_customer_receipts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(CustomerReceipt).all()