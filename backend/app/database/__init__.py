from app.database.connection import engine
from app.database.base import Base

from app.models.company import Company
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.purchase_return import PurchaseReturn
from app.models.purchase_return_item import PurchaseReturnItem


def init_db():
    Base.metadata.create_all(bind=engine)