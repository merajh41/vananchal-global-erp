from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db

from app.models.user import User

from app.schemas.report import (
    DashboardResponse,
    OutstandingItem,
    StockSummaryItem,
)

from app.services.report_service import ReportService


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get(
    "/dashboard",
    response_model=DashboardResponse,
)
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReportService.dashboard(db)


@router.get(
    "/customer-outstanding",
    response_model=list[OutstandingItem],
)
def customer_outstanding(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReportService.customer_outstanding(db)


@router.get(
    "/supplier-outstanding",
    response_model=list[OutstandingItem],
)
def supplier_outstanding(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReportService.supplier_outstanding(db)


@router.get(
    "/current-stock",
    response_model=list[StockSummaryItem],
)
def current_stock(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReportService.current_stock(db)


@router.get(
    "/low-stock",
    response_model=list[StockSummaryItem],
)
def low_stock(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReportService.low_stock(db)


@router.get(
    "/out-of-stock",
    response_model=list[StockSummaryItem],
)
def out_of_stock(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReportService.out_of_stock(db)