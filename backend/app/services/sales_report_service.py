from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.product import Product


class SalesReportService:

    @staticmethod
    def monthly_sales(db: Session):

        rows = (
            db.query(
                func.strftime("%Y-%m", Sale.sale_date).label("month"),
                func.sum(Sale.total_amount).label("total"),
            )
            .group_by(func.strftime("%Y-%m", Sale.sale_date))
            .order_by(func.strftime("%Y-%m", Sale.sale_date))
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
    def top_selling_products(
        db: Session,
        limit: int = 10,
    ):

        rows = (
            db.query(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                func.sum(SaleItem.quantity).label("quantity"),
                func.sum(SaleItem.amount).label("amount"),
            )
            .join(
                SaleItem,
                Product.id == SaleItem.product_id,
            )
            .group_by(
                Product.id,
                Product.name,
            )
            .order_by(
                func.sum(SaleItem.quantity).desc()
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