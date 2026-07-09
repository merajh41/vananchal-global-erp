from datetime import date
from typing import Optional

from pydantic import BaseModel


class BankTransactionCreate(BaseModel):
    bank_account_id: int
    transaction_date: date
    transaction_type: str
    amount: float
    reference_no: Optional[str] = None
    remarks: Optional[str] = None


class BankTransactionResponse(BaseModel):
    id: int
    bank_account_id: int
    transaction_date: date
    transaction_type: str
    amount: float
    reference_no: Optional[str]
    remarks: Optional[str]
    created_by: int

    class Config:
        from_attributes = True