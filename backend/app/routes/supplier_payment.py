from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.auth.dependencies import get_current_user
from app.auth.roles import require_role

from app.models.supplier_payment import SupplierPayment
from app.models.user import User

from app.schemas.supplier_payment import (
    SupplierPaymentCreate,
    SupplierPaymentResponse,
)

from app.services.supplier_payment_service import SupplierPaymentService


router = APIRouter(
    prefix="/supplier-payments",
    tags=["Supplier Payments"],
)


@router.post("/", response_model=SupplierPaymentResponse)
def create_supplier_payment(
    payment: SupplierPaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return SupplierPaymentService.create_payment(
        db=db,
        payment=payment,
        current_user=current_user,
    )


@router.get("/", response_model=list[SupplierPaymentResponse])
def get_supplier_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(SupplierPayment).all()