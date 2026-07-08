from datetime import date
from pydantic import BaseModel


class SupplierLedgerEntry(BaseModel):
    date: date
    transaction_type: str
    reference: str
    debit: float
    credit: float
    balance: float


class SupplierLedgerResponse(BaseModel):
    supplier_id: int

    total_purchase: float
    total_payment: float
    outstanding: float

    ledger: list[SupplierLedgerEntry]