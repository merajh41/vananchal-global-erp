from datetime import date
from pydantic import BaseModel


class SaleItemCreate(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: float
    rate: float


class SaleItemResponse(BaseModel):
    id: int
    product_id: int
    warehouse_id: int
    quantity: float
    rate: float
    amount: float

    class Config:
        from_attributes = True


class SaleCreate(BaseModel):
    customer_id: int
    sale_date: date
    remarks: str | None = None
    items: list[SaleItemCreate]


class SaleResponse(BaseModel):
    id: int
    invoice_no: str
    customer_id: int
    sale_date: date
    total_amount: float
    remarks: str | None = None
    created_by: int
    items: list[SaleItemResponse]

    class Config:
        from_attributes = True