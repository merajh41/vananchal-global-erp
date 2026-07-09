from datetime import date
from typing import Optional

from pydantic import BaseModel


class IncomeCreate(BaseModel):
    income_date: date
    category: str
    amount: float
    payment_mode: str
    reference_no: Optional[str] = None
    remarks: Optional[str] = None


class IncomeResponse(BaseModel):
    id: int
    income_date: date
    category: str
    amount: float
    payment_mode: str
    reference_no: Optional[str]
    remarks: Optional[str]
    created_by: int

    class Config:
        from_attributes = True