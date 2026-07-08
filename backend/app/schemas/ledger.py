from datetime import date
from pydantic import BaseModel


class LedgerEntry(BaseModel):
    date: date
    transaction_type: str
    reference: str
    debit: float
    credit: float
    balance: float


class CustomerLedgerResponse(BaseModel):
    customer_id: int

    total_sales: float
    total_receipts: float
    outstanding: float

    ledger: list[LedgerEntry]