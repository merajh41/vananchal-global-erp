from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.roles import require_role
from app.database.connection import get_db

from app.models.expense import Expense
from app.models.user import User

from app.schemas.expense import (
    ExpenseCreate,
    ExpenseResponse,
)

from app.services.expense_service import ExpenseService


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
)


@router.post(
    "/",
    response_model=ExpenseResponse,
)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return ExpenseService.create(
        db=db,
        expense=expense,
        current_user=current_user,
    )


@router.get(
    "/",
    response_model=list[ExpenseResponse],
)
def get_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return db.query(Expense).all()