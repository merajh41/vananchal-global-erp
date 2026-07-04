from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user
from app.auth.roles import require_role
from app.models.user import User
from app.models.supplier import Supplier
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.models.stock_ledger import StockLedger
from app.services.stock_service import StockService
from app.schemas.purchase import (
    PurchaseCreate,
    PurchaseResponse,
)

router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)


@router.post("/", response_model=PurchaseResponse)
def create_purchase(
    purchase: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):

    print("=" * 60)
    print("PURCHASE REQUEST RECEIVED")
    print(purchase.model_dump())
    print("Items:", purchase.items)
    print("Items Count:", len(purchase.items))
    print("=" * 60)

    supplier = db.query(Supplier).filter(
        Supplier.id == purchase.supplier_id
    ).first()

    if not supplier:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found"
        )

    invoice_no = f"PUR-{datetime.now().year}-{db.query(Purchase).count()+1:05d}"

    db_purchase = Purchase(
        invoice_no=invoice_no,
        supplier_id=purchase.supplier_id,
        purchase_date=purchase.purchase_date,
        remarks=purchase.remarks,
        created_by=current_user.id,
        total_amount=0
    )

    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)

    total = 0

    for item in purchase.items:

        print("\nProcessing Item")
        print(item)

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found"
            )

        warehouse = db.query(Warehouse).filter(
            Warehouse.id == item.warehouse_id
        ).first()

        if not warehouse:
            raise HTTPException(
                status_code=404,
                detail=f"Warehouse {item.warehouse_id} not found"
            )

        amount = item.quantity * item.rate

        print("Amount:", amount)

        purchase_item = PurchaseItem(
            purchase_id=db_purchase.id,
            product_id=item.product_id,
            warehouse_id=item.warehouse_id,
            quantity=item.quantity,
            rate=item.rate,
            amount=amount
        )

        db.add(purchase_item)

        StockService.add_stock(
    db=db,
    product_id=item.product_id,
    warehouse_id=item.warehouse_id,
    quantity=item.quantity,
    transaction_type="PURCHASE",
    remarks=invoice_no,
)

        total += amount

        print("Running Total:", total)

    db_purchase.total_amount = total

    db.commit()
    db.refresh(db_purchase)

    print("=" * 60)
    print("PURCHASE SAVED")
    print("Invoice:", invoice_no)
    print("Total:", total)
    print("=" * 60)

    return db_purchase


@router.get("/", response_model=list[PurchaseResponse])
def get_purchases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return db.query(Purchase).all()