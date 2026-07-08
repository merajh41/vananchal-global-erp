from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.auth.dependencies import get_current_user

from app.models.user import User

from app.schemas.supplier_ledger import (
    SupplierLedgerResponse,
)

from app.services.supplier_ledger_service import (
    SupplierLedgerService,
)


router = APIRouter(
    prefix="/supplier-ledger",
    tags=["Supplier Ledger"],
)


@router.get(
    "/{supplier_id}",
    response_model=SupplierLedgerResponse,
)
def supplier_ledger(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SupplierLedgerService.supplier_ledger(
        db=db,
        supplier_id=supplier_id,
    )