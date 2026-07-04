from sqlalchemy.orm import Session

from app.models.stock_ledger import StockLedger


class StockService:

    @staticmethod
    def add_stock(
        db: Session,
        product_id: int,
        warehouse_id: int,
        quantity: float,
        transaction_type: str,
        remarks: str,
    ):
        stock = StockLedger(
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity=quantity,
            transaction_type=transaction_type,
            remarks=remarks,
        )

        db.add(stock)
        return stock

    @staticmethod
    def remove_stock(
        db: Session,
        product_id: int,
        warehouse_id: int,
        quantity: float,
        transaction_type: str,
        remarks: str,
    ):
        stock = StockLedger(
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity=-quantity,
            transaction_type=transaction_type,
            remarks=remarks,
        )

        db.add(stock)
        return stock