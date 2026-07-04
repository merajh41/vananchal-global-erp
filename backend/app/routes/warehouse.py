from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user
from app.auth.roles import require_role

from app.models.warehouse import Warehouse
from app.models.user import User

from app.schemas.warehouse import (
    WarehouseCreate,
    WarehouseResponse
)

router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"]
)


@router.post("/", response_model=WarehouseResponse)
def create_warehouse(
    warehouse: WarehouseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):

    db_warehouse = Warehouse(**warehouse.model_dump())

    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)

    return db_warehouse


@router.get("/", response_model=list[WarehouseResponse])
def get_warehouses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return db.query(Warehouse).all()