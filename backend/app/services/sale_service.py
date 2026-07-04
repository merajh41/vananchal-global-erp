from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.product import Product
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.user import User
from app.models.warehouse import Warehouse

from app.schemas.sale import SaleCreate

from app.services.inventory_service import InventoryService


class SaleService:

    @staticmethod
    def create_sale(
        db: Session,
        sale: SaleCreate,
        current_user: User,
    ):

        customer = (
            db.query(Customer)
            .filter(Customer.id == sale.customer_id)
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        invoice_no = (
            f"SAL-{datetime.now().year}-"
            f"{db.query(Sale).count() + 1:05d}"
        )

        db_sale = Sale(
            invoice_no=invoice_no,
            customer_id=sale.customer_id,
            sale_date=sale.sale_date,
            remarks=sale.remarks,
            created_by=current_user.id,
            total_amount=0,
        )

        db.add(db_sale)
        db.flush()

        total = 0

        for item in sale.items:

            product = (
                db.query(Product)
                .filter(Product.id == item.product_id)
                .first()
            )

            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product {item.product_id} not found"
                )

            warehouse = (
                db.query(Warehouse)
                .filter(Warehouse.id == item.warehouse_id)
                .first()
            )

            if not warehouse:
                raise HTTPException(
                    status_code=404,
                    detail=f"Warehouse {item.warehouse_id} not found"
                )

            try:
                InventoryService.decrease_stock(
                    db=db,
                    product_id=item.product_id,
                    warehouse_id=item.warehouse_id,
                    quantity=item.quantity,
                    remarks=invoice_no,
                    transaction_type="SALE",
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=400,
                    detail=str(e)
                )

            amount = item.quantity * item.rate

            db_item = SaleItem(
                sale_id=db_sale.id,
                product_id=item.product_id,
                warehouse_id=item.warehouse_id,
                quantity=item.quantity,
                rate=item.rate,
                amount=amount,
            )

            db.add(db_item)

            total += amount

        db_sale.total_amount = total

        db.commit()
        db.refresh(db_sale)

        return db_sale