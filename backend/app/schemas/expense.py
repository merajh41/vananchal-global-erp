from datetime import date
from typing import Optional

from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    expense_date: date
    category: str
    amount: float
    payment_mode: str
    reference_no: Optional[str] = None
    remarks: Optional[str] = None


class ExpenseResponse(BaseModel):
    id: int
    expense_date: date
    category: str
    amount: float
    payment_mode: str
    reference_no: Optional[str]
    remarks: Optional[str]
    created_by: int

    class Config:
        from_attributes = True
    