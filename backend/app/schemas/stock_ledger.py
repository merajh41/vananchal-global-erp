from pydantic import BaseModel


class StockLedgerCreate(BaseModel):
    product_id: int
    warehouse_id: int
    transaction_type: str
    quantity: float
    remarks: str | None = None


class StockLedgerResponse(BaseModel):
    id: int
    product_id: int
    warehouse_id: int
    transaction_type: str
    quantity: float
    remarks: str | None = None

    class Config:
        from_attributes = True