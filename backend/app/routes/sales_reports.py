from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User

from app.schemas.report import (
    MonthlyReportItem,
    ProductSummaryItem,
)

from app.services.sales_report_service import SalesReportService


router = APIRouter(
    prefix="/sales-reports",
    tags=["Sales Reports"],
)


@router.get(
    "/monthly",
    response_model=list[MonthlyReportItem],
)
def monthly_sales(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SalesReportService.monthly_sales(db)


@router.get(
    "/top-products",
    response_model=list[ProductSummaryItem],
)
def top_products(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SalesReportService.top_selling_products(
        db=db,
        limit=limit,
    )