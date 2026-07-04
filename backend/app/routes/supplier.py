from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user
from app.auth.roles import require_role

from app.models.supplier import Supplier
from app.models.user import User

from app.schemas.supplier import (
    SupplierCreate,
    SupplierResponse
)

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"]
)


@router.post("/", response_model=SupplierResponse)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):

    existing_supplier = db.query(Supplier).filter(
        Supplier.name == supplier.name
    ).first()

    if existing_supplier:
        raise HTTPException(
            status_code=400,
            detail="Supplier already exists."
        )

    db_supplier = Supplier(**supplier.model_dump())

    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)

    return db_supplier


@router.get("/", response_model=list[SupplierResponse])
def get_suppliers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return db.query(Supplier).all()


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    supplier = db.query(Supplier).filter(
        Supplier.id == supplier_id
    ).first()

    if not supplier:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found."
        )

    return supplier