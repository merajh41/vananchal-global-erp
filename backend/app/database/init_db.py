from app.database.connection import engine
from app.database.base import Base

# Import ALL models here
from app.models.company import Company
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.stock_ledger import StockLedger
from app.models.supplier import Supplier
from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.models.customer import Customer
from app.models.sale import Sale
from app.models.sale_item import SaleItem
def init_db():
    Base.metadata.create_all(bind=engine)