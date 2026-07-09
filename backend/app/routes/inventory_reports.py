from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User

from app.schemas.report import (
    StockSummaryItem,
    StockValueItem,
)

from app.services.inventory_report_service import (
    InventoryReportService,
)


router = APIRouter(
    prefix="/inventory-reports",
    tags=["Inventory Reports"],
)


@router.get(
    "/current-stock",
    response_model=list[StockSummaryItem],
)
def current_stock(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return InventoryReportService.current_stock(db)


@router.get(
    "/low-stock",
    response_model=list[StockSummaryItem],
)
def low_stock(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return InventoryReportService.low_stock(db)


@router.get(
    "/out-of-stock",
    response_model=list[StockSummaryItem],
)
def out_of_stock(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return InventoryReportService.out_of_stock(db)


@router.get(
    "/stock-value",
    response_model=list[StockValueItem],
)
def stock_value(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return InventoryReportService.stock_value(db)