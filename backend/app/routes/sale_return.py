from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.auth.dependencies import get_current_user
from app.auth.roles import require_role

from app.models.sale_return import SaleReturn
from app.models.user import User

from app.schemas.sale_return import (
    SaleReturnCreate,
    SaleReturnResponse,
)

from app.services.sale_return_service import SaleReturnService


router = APIRouter(
    prefix="/sale-returns",
    tags=["Sale Returns"],
)


@router.post("/", response_model=SaleReturnResponse)
def create_sale_return(
    sale_return: SaleReturnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return SaleReturnService.create_sale_return(
        db=db,
        sale_return=sale_return,
        current_user=current_user,
    )


@router.get("/", response_model=list[SaleReturnResponse])
def get_sale_returns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(SaleReturn).all()