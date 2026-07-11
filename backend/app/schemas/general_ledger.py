from datetime import date
from typing import Optional

from pydantic import BaseModel


class GeneralLedgerEntry(BaseModel):
    date: date
    account: str
    debit: float
    credit: float
    balance: float
    narration: Optional[str]
    reference_no: Optional[str]

    class Config:
        from_attributes = True