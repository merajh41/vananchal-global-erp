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
from app.models.customer import Customer

from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem

from app.models.purchase_return import PurchaseReturn
from app.models.purchase_return_item import PurchaseReturnItem

from app.models.sale import Sale
from app.models.sale_item import SaleItem

from app.models.sale_return import SaleReturn
from app.models.sale_return_item import SaleReturnItem
from app.models.supplier_payment import SupplierPayment
from app.models.customer_receipt import CustomerReceipt
from app.models.expense import Expense
from app.models.income import Income
from app.models.bank_account import BankAccount
from app.models.bank_transaction import BankTransaction
def init_db():
    Base.metadata.create_all(bind=engine)