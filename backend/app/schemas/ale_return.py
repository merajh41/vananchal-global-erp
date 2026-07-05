from datetime import date
from pydantic import BaseModel


class SaleReturnItemCreate(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: float
    rate: float


class SaleReturnItemResponse(BaseModel):
    id: int
    product_id: int
    warehouse_id: int
    quantity: float
    rate: float
    amount: float

    class Config:
        from_attributes = True


class SaleReturnCreate(BaseModel):
    customer_id: int
    return_date: date
    remarks: str | None = None
    items: list[SaleReturnItemCreate]


class SaleReturnResponse(BaseModel):
    id: int
    return_no: str
    customer_id: int
    return_date: date
    total_amount: float
    remarks: str | None = None
    created_by: int
    items: list[SaleReturnItemResponse]

    class Config:
        from_attributes = True