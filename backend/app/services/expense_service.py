from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseCreate


class ExpenseService:

    @staticmethod
    def create(
        db: Session,
        expense: ExpenseCreate,
        current_user: User,
    ):

        db_expense = Expense(
            expense_date=expense.expense_date,
            category=expense.category,
            amount=expense.amount,
            payment_mode=expense.payment_mode,
            reference_no=expense.reference_no,
            remarks=expense.remarks,
            created_by=current_user.id,
        )

        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)

        return db_expense