from datetime import date
from pydantic import BaseModel


class CustomerReceiptCreate(BaseModel):
    customer_id: int
    receipt_date: date
    amount: float
    payment_mode: str
    reference_no: str | None = None
    remarks: str | None = None


class CustomerReceiptResponse(BaseModel):
    id: int
    customer_id: int
    receipt_date: date
    amount: float
    payment_mode: str
    reference_no: str | None = None
    remarks: str | None = None
    created_by: int

    class Config:
        from_attributes = True