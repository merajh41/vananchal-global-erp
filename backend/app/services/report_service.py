from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.customer_receipt import CustomerReceipt
from app.models.product import Product
from app.models.purchase import Purchase
from app.models.sale import Sale
from app.models.stock_ledger import StockLedger
from app.models.supplier import Supplier
from app.models.supplier_payment import SupplierPayment

from app.services.ledger_service import LedgerService
from app.services.supplier_ledger_service import SupplierLedgerService


class ReportService:

    @staticmethod
    def dashboard(db: Session):

        today = date.today()

        today_sales = (
            db.query(func.sum(Sale.total_amount))
            .filter(Sale.sale_date == today)
            .scalar()
            or 0
        )

        today_purchase = (
            db.query(func.sum(Purchase.total_amount))
            .filter(Purchase.purchase_date == today)
            .scalar()
            or 0
        )

        month_sales = (
            db.query(func.sum(Sale.total_amount))
            .filter(
                func.strftime("%Y-%m", Sale.sale_date)
                == today.strftime("%Y-%m")
            )
            .scalar()
            or 0
        )

        month_purchase = (
            db.query(func.sum(Purchase.total_amount))
            .filter(
                func.strftime("%Y-%m", Purchase.purchase_date)
                == today.strftime("%Y-%m")
            )
            .scalar()
            or 0
        )

        customer_sales = (
            db.query(func.sum(Sale.total_amount)).scalar() or 0
        )

        customer_receipts = (
            db.query(func.sum(CustomerReceipt.amount)).scalar() or 0
        )

        supplier_purchase = (
            db.query(func.sum(Purchase.total_amount)).scalar() or 0
        )

        supplier_payment = (
            db.query(func.sum(SupplierPayment.amount)).scalar() or 0
        )

        stock_value = 0
        low_stock_items = 0
        out_of_stock_items = 0

        products = db.query(Product).all()

        for product in products:

            stock = (
                db.query(func.sum(StockLedger.quantity))
                .filter(
                    StockLedger.product_id == product.id
                )
                .scalar()
                or 0
            )

            stock_value += stock * product.purchase_price

            if stock <= 0:
                out_of_stock_items += 1
            elif stock < 10:
                low_stock_items += 1

        return {
            "today_sales": today_sales,
            "today_purchase": today_purchase,
            "month_sales": month_sales,
            "month_purchase": month_purchase,
            "stock_value": stock_value,
            "customer_outstanding": customer_sales - customer_receipts,
            "supplier_outstanding": supplier_purchase - supplier_payment,
            "total_products": db.query(Product).count(),
            "total_customers": db.query(Customer).count(),
            "total_suppliers": db.query(Supplier).count(),
            "low_stock_items": low_stock_items,
            "out_of_stock_items": out_of_stock_items,
        }

    @staticmethod
    def customer_outstanding(db: Session):

        customers = db.query(Customer).all()

        data = []

        for customer in customers:

            ledger = LedgerService.customer_ledger(
                db,
                customer.id,
            )

            data.append(
                {
                    "id": customer.id,
                    "name": customer.name,
                    "outstanding": ledger["outstanding"],
                }
            )

        return data

    @staticmethod
    def supplier_outstanding(db: Session):

        suppliers = db.query(Supplier).all()

        data = []

        for supplier in suppliers:

            ledger = SupplierLedgerService.supplier_ledger(
                db,
                supplier.id,
            )

            data.append(
                {
                    "id": supplier.id,
                    "name": supplier.name,
                    "outstanding": ledger["outstanding"],
                }
            )

        return data

    @staticmethod
    def current_stock(db: Session):

        data = []

        products = db.query(Product).all()

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
            for item in ReportService.current_stock(db)
            if 0 < item["stock"] < 10
        ]

    @staticmethod
    def out_of_stock(db: Session):

        return [
            item
            for item in ReportService.current_stock(db)
            if item["stock"] <= 0
        ]