from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.roles import require_role
from app.database.connection import get_db

from app.models.income import Income
from app.models.user import User

from app.schemas.income import (
    IncomeCreate,
    IncomeResponse,
)

from app.services.income_service import IncomeService


router = APIRouter(
    prefix="/incomes",
    tags=["Income"],
)


@router.post(
    "/",
    response_model=IncomeResponse,
)
def create_income(
    income: IncomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return IncomeService.create(
        db=db,
        income=income,
        current_user=current_user,
    )


@router.get(
    "/",
    response_model=list[IncomeResponse],
)
def get_incomes(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return db.query(Income).all()