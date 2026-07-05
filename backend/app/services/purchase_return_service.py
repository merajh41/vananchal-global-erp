from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.supplier import Supplier
from app.models.product import Product
from app.models.warehouse import Warehouse

from app.models.purchase_return import PurchaseReturn
from app.models.purchase_return_item import PurchaseReturnItem

from app.schemas.purchase_return import PurchaseReturnCreate

from app.services.inventory_service import InventoryService


class PurchaseReturnService:

    @staticmethod
    def create_purchase_return(
        db: Session,
        purchase_return: PurchaseReturnCreate,
        current_user: User,
    ):

        supplier = (
            db.query(Supplier)
            .filter(
                Supplier.id == purchase_return.supplier_id
            )
            .first()
        )

        if not supplier:
            raise HTTPException(
                status_code=404,
                detail="Supplier not found"
            )

        return_no = (
            f"PR-{datetime.now().year}-"
            f"{db.query(PurchaseReturn).count() + 1:05d}"
        )

        db_return = PurchaseReturn(
            return_no=return_no,
            supplier_id=purchase_return.supplier_id,
            return_date=purchase_return.return_date,
            remarks=purchase_return.remarks,
            created_by=current_user.id,
            total_amount=0,
        )

        db.add(db_return)
        db.flush()

        total = 0

        for item in purchase_return.items:

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
                    transaction_type="PURCHASE_RETURN",
                    remarks=return_no,
                )

            except ValueError as e:
                raise HTTPException(
                    status_code=400,
                    detail=str(e)
                )

            amount = item.quantity * item.rate

            purchase_return_item = PurchaseReturnItem(
                purchase_return_id=db_return.id,
                product_id=item.product_id,
                warehouse_id=item.warehouse_id,
                quantity=item.quantity,
                rate=item.rate,
                amount=amount,
            )

            db.add(purchase_return_item)

            total += amount

        db_return.total_amount = total

        db.commit()
        db.refresh(db_return)

        return db_return