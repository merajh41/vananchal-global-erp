from fastapi import FastAPI

from app.config import settings
from app.database.init_db import init_db

from app.routes.auth import router as auth_router
from app.routes.company import router as company_router
from app.routes.users import router as users_router
from app.routes.category import router as category_router
from app.routes.product import router as product_router
from app.routes.warehouse import router as warehouse_router
from app.routes.stock import router as stock_router
from app.routes.supplier import router as supplier_router
from app.routes.purchase import router as purchase_router
from app.routes.customer import router as customer_router
from app.routes.sale import router as sale_router
from app.routes.purchase_return import router as purchase_return_router
from app.routes.sale_return import router as sale_return_router
from app.routes.supplier_payment import router as supplier_payment_router
from app.routes.customer_receipt import router as customer_receipt_router
from app.routes.ledger import router as ledger_router
from app.routes.supplier_ledger import router as supplier_ledger_router
from app.routes.reports import router as reports_router
from app.routes.sales_reports import router as sales_reports_router
from app.routes.purchase_reports import router as purchase_reports_router
from app.routes.inventory_reports import router as inventory_reports_router
from app.routes.expense import router as expense_router
from app.routes.income import router as income_router
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(auth_router)
app.include_router(company_router)
app.include_router(users_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(warehouse_router)
app.include_router(stock_router)
app.include_router(supplier_router)
app.include_router(purchase_router)
app.include_router(customer_router)
app.include_router(sale_router)
app.include_router(purchase_return_router)
app.include_router(sale_return_router)
app.include_router(supplier_payment_router)
app.include_router(customer_receipt_router)
app.include_router(ledger_router)
app.include_router(supplier_ledger_router)
app.include_router(reports_router)
app.include_router(sales_reports_router)
app.include_router(purchase_reports_router)
app.include_router(inventory_reports_router)
app.include_router(expense_router)
app.include_router(income_router)
@app.get("/")
def home():
    return {
        "application": settings.APP_NAME,
        "company": settings.COMPANY_NAME,
        "status": "Running Successfully",
        "version": settings.VERSION,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }