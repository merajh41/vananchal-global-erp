from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User

from app.schemas.report import (
    MonthlyReportItem,
    ProductSummaryItem,
)

from app.services.purchase_report_service import PurchaseReportService


router = APIRouter(
    prefix="/purchase-reports",
    tags=["Purchase Reports"],
)


@router.get(
    "/monthly",
    response_model=list[MonthlyReportItem],
)
def monthly_purchase(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PurchaseReportService.monthly_purchases(db)


@router.get(
    "/top-products",
    response_model=list[ProductSummaryItem],
)
def top_products(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PurchaseReportService.top_purchased_products(
        db=db,
        limit=limit,
    )