from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.auth.dependencies import get_current_user
from app.auth.roles import require_role

from app.models.sale import Sale
from app.models.user import User

from app.schemas.sale import (
    SaleCreate,
    SaleResponse,
)

from app.services.sale_service import SaleService


router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)


@router.post("/", response_model=SaleResponse)
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return SaleService.create_sale(
        db=db,
        sale=sale,
        current_user=current_user,
    )


@router.get("/", response_model=list[SaleResponse])
def get_sales(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Sale).all()