from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    category_id: int
    unit: str
    purchase_price: float
    selling_price: float
    opening_stock: float


class ProductResponse(BaseModel):
    id: int
    name: str
    category_id: int
    unit: str
    purchase_price: float
    selling_price: float
    opening_stock: float

    class Config:
        from_attributes = True