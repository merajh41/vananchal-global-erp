from pydantic import BaseModel


class DashboardResponse(BaseModel):
    today_sales: float
    today_purchase: float

    month_sales: float
    month_purchase: float

    stock_value: float

    customer_outstanding: float
    supplier_outstanding: float

    total_products: int
    total_customers: int
    total_suppliers: int

    low_stock_items: int
    out_of_stock_items: int


class OutstandingItem(BaseModel):
    id: int
    name: str
    outstanding: float


class StockSummaryItem(BaseModel):
    product_id: int
    product_name: str
    warehouse_name: str
    stock: float


class StockValueItem(BaseModel):
    product_id: int
    product_name: str
    stock: float
    purchase_price: float
    stock_value: float