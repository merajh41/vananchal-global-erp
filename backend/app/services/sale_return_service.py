from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.user import User

from app.models.sale_return import SaleReturn
from app.models.sale_return_item import SaleReturnItem

from app.schemas.sale_return import SaleReturnCreate

from app.services.inventory_service import InventoryService


class SaleReturnService:

    @staticmethod
    def create_sale_return(
        db: Session,
        sale_return: SaleReturnCreate,
        current_user: User,
    ):

        customer = (
            db.query(Customer)
            .filter(Customer.id == sale_return.customer_id)
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return_no = (
            f"SR-{datetime.now().year}-"
            f"{db.query(SaleReturn).count()+1:05d}"
        )

        db_return = SaleReturn(
            return_no=return_no,
            customer_id=sale_return.customer_id,
            return_date=sale_return.return_date,
            remarks=sale_return.remarks,
            created_by=current_user.id,
            total_amount=0,
        )

        db.add(db_return)
        db.flush()

        total = 0

        for item in sale_return.items:

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

            InventoryService.increase_stock(
                db=db,
                product_id=item.product_id,
                warehouse_id=item.warehouse_id,
                quantity=item.quantity,
                remarks=return_no,
                transaction_type="SALE_RETURN",
            )

            amount = item.quantity * item.rate

            db_item = SaleReturnItem(
                sale_return_id=db_return.id,
                product_id=item.product_id,
                warehouse_id=item.warehouse_id,
                quantity=item.quantity,
                rate=item.rate,
                amount=amount,
            )

            db.add(db_item)

            total += amount

        db_return.total_amount = total

        db.commit()
        db.refresh(db_return)

        return db_return