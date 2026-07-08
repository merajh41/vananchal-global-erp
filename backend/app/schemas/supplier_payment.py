from datetime import date
from pydantic import BaseModel


class SupplierPaymentCreate(BaseModel):
    supplier_id: int
    payment_date: date
    amount: float
    payment_mode: str
    reference_no: str | None = None
    remarks: str | None = None


class SupplierPaymentResponse(BaseModel):
    id: int
    supplier_id: int
    payment_date: date
    amount: float
    payment_mode: str
    reference_no: str | None = None
    remarks: str | None = None
    created_by: int

    class Config:
        from_attributes = True