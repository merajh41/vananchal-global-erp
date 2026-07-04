from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.connection import get_db
from app.auth.dependencies import get_current_user
from app.auth.roles import require_role

from app.models.stock_ledger import StockLedger
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.user import User

from app.schemas.stock_ledger import (
    StockLedgerCreate,
    StockLedgerResponse
)

router = APIRouter(
    prefix="/stock",
    tags=["Stock Ledger"]
)


@router.post("/", response_model=StockLedgerResponse)
def create_stock_entry(
    entry: StockLedgerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):

    product = db.query(Product).filter(
        Product.id == entry.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    warehouse = db.query(Warehouse).filter(
        Warehouse.id == entry.warehouse_id
    ).first()

    if not warehouse:
        raise HTTPException(
            status_code=404,
            detail="Warehouse not found"
        )

    stock = StockLedger(**entry.model_dump())

    db.add(stock)
    db.commit()
    db.refresh(stock)

    return stock


@router.get("/", response_model=list[StockLedgerResponse])
def get_stock_entries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return db.query(StockLedger).all()


@router.get("/current")
def current_stock(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = (
        db.query(
            Product.id.label("product_id"),
            Product.name.label("product"),
            Warehouse.name.label("warehouse"),
            func.sum(StockLedger.quantity).label("stock"),
        )
        .join(Product, StockLedger.product_id == Product.id)
        .join(Warehouse, StockLedger.warehouse_id == Warehouse.id)
        .group_by(
            Product.id,
            Product.name,
            Warehouse.name
        )
        .all()
    )

    return [
        {
            "product_id": row.product_id,
            "product": row.product,
            "warehouse": row.warehouse,
            "stock": row.stock,
        }
        for row in result
    ]