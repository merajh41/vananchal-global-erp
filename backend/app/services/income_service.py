from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.user import User
from app.schemas.income import IncomeCreate


class IncomeService:

    @staticmethod
    def create(
        db: Session,
        income: IncomeCreate,
        current_user: User,
    ):

        db_income = Income(
            income_date=income.income_date,
            category=income.category,
            amount=income.amount,
            payment_mode=income.payment_mode,
            reference_no=income.reference_no,
            remarks=income.remarks,
            created_by=current_user.id,
        )

        db.add(db_income)
        db.commit()
        db.refresh(db_income)

        return db_income