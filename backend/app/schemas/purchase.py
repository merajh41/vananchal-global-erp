from datetime import date
from pydantic import BaseModel


class PurchaseItemCreate(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: float
    rate: float


class PurchaseItemResponse(BaseModel):
    id: int
    product_id: int
    warehouse_id: int
    quantity: float
    rate: float
    amount: float

    class Config:
        from_attributes = True


class PurchaseCreate(BaseModel):
    supplier_id: int
    purchase_date: date
    remarks: str | None = None
    items: list[PurchaseItemCreate]


class PurchaseResponse(BaseModel):
    id: int
    invoice_no: str
    supplier_id: int
    purchase_date: date
    total_amount: float
    remarks: str | None = None
    created_by: int
    items: list[PurchaseItemResponse]

    class Config:
        from_attributes = True