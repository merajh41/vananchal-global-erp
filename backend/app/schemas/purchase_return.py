from datetime import date
from pydantic import BaseModel


class PurchaseReturnItemCreate(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: float
    rate: float


class PurchaseReturnItemResponse(BaseModel):
    id: int
    product_id: int
    warehouse_id: int
    quantity: float
    rate: float
    amount: float

    class Config:
        from_attributes = True


class PurchaseReturnCreate(BaseModel):
    supplier_id: int
    return_date: date
    remarks: str | None = None
    items: list[PurchaseReturnItemCreate]


class PurchaseReturnResponse(BaseModel):
    id: int
    return_no: str
    supplier_id: int
    return_date: date
    total_amount: float
    remarks: str | None = None
    created_by: int
    items: list[PurchaseReturnItemResponse]

    class Config:
        from_attributes = True