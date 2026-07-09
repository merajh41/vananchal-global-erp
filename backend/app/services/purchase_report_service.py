from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.models.product import Product


class PurchaseReportService:

    @staticmethod
    def monthly_purchases(db: Session):

        rows = (
            db.query(
                func.strftime("%Y-%m", Purchase.purchase_date).label("month"),
                func.sum(Purchase.total_amount).label("total"),
            )
            .group_by(
                func.strftime("%Y-%m", Purchase.purchase_date)
            )
            .order_by(
                func.strftime("%Y-%m", Purchase.purchase_date)
            )
            .all()
        )

        return [
            {
                "month": row.month,
                "total": row.total or 0,
            }
            for row in rows
        ]

    @staticmethod
    def top_purchased_products(
        db: Session,
        limit: int = 10,
    ):

        rows = (
            db.query(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                func.sum(PurchaseItem.quantity).label("quantity"),
                func.sum(PurchaseItem.amount).label("amount"),
            )
            .join(
                PurchaseItem,
                Product.id == PurchaseItem.product_id,
            )
            .group_by(
                Product.id,
                Product.name,
            )
            .order_by(
                func.sum(PurchaseItem.quantity).desc()
            )
            .limit(limit)
            .all()
        )

        return [
            {
                "product_id": row.product_id,
                "product_name": row.product_name,
                "quantity": row.quantity or 0,
                "amount": row.amount or 0,
            }
            for row in rows
        ]