from fastapi import APIRouter

from app.constants.chart_of_accounts import ACCOUNT_TYPES


router = APIRouter(
    prefix="/accounting/master",
    tags=["Accounting"],
)


@router.get("/account-types")
def get_account_types():
    return ACCOUNT_TYPES