from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.stock_ledger import StockLedger


class InventoryReportService:

    LOW_STOCK_LIMIT = 10

    @staticmethod
    def current_stock(db: Session):

        products = db.query(Product).all()

        data = []

        for product in products:

            stock = (
                db.query(func.sum(StockLedger.quantity))
                .filter(
                    StockLedger.product_id == product.id
                )
                .scalar()
                or 0
            )

            data.append(
                {
                    "product_id": product.id,
                    "product_name": product.name,
                    "warehouse_name": "All Warehouses",
                    "stock": stock,
                }
            )

        return data

    @staticmethod
    def low_stock(db: Session):

        return [
            item
            for item in InventoryReportService.current_stock(db)
            if 0 < item["stock"] < InventoryReportService.LOW_STOCK_LIMIT
        ]

    @staticmethod
    def out_of_stock(db: Session):

        return [
            item
            for item in InventoryReportService.current_stock(db)
            if item["stock"] <= 0
        ]

    @staticmethod
    def stock_value(db: Session):

        products = db.query(Product).all()

        data = []

        for product in products:

            stock = (
                db.query(func.sum(StockLedger.quantity))
                .filter(
                    StockLedger.product_id == product.id
                )
                .scalar()
                or 0
            )

            data.append(
                {
                    "product_id": product.id,
                    "product_name": product.name,
                    "stock": stock,
                    "purchase_price": product.purchase_price,
                    "stock_value": stock * product.purchase_price,
                }
            )

        return data