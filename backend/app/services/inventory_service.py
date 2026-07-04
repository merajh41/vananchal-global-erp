from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.stock_ledger import StockLedger


class InventoryService:

    @staticmethod
    def get_current_stock(
        db: Session,
        product_id: int,
        warehouse_id: int,
    ) -> float:

        stock = (
            db.query(func.sum(StockLedger.quantity))
            .filter(
                StockLedger.product_id == product_id,
                StockLedger.warehouse_id == warehouse_id,
            )
            .scalar()
        )

        return stock or 0

    @staticmethod
    def has_sufficient_stock(
        db: Session,
        product_id: int,
        warehouse_id: int,
        required_qty: float,
    ) -> bool:

        current = InventoryService.get_current_stock(
            db,
            product_id,
            warehouse_id,
        )

        return current >= required_qty

    @staticmethod
    def increase_stock(
        db: Session,
        product_id: int,
        warehouse_id: int,
        quantity: float,
        remarks: str,
        transaction_type: str = "IN",
    ):

        from app.services.stock_service import StockService

        return StockService.add_stock(
            db=db,
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity=quantity,
            transaction_type=transaction_type,
            remarks=remarks,
        )

    @staticmethod
    def decrease_stock(
        db: Session,
        product_id: int,
        warehouse_id: int,
        quantity: float,
        remarks: str,
        transaction_type: str = "OUT",
    ):

        from app.services.stock_service import StockService

        if not InventoryService.has_sufficient_stock(
            db,
            product_id,
            warehouse_id,
            quantity,
        ):
            raise ValueError("Insufficient stock.")

        return StockService.remove_stock(
            db=db,
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity=quantity,
            transaction_type=transaction_type,
            remarks=remarks,
        )