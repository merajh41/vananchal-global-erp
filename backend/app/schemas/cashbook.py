from datetime import date

from pydantic import BaseModel


class CashBookEntry(BaseModel):
    date: date
    type: str
    description: str
    receipt: float
    payment: float
    balance: float

    class Config:
        from_attributes = True