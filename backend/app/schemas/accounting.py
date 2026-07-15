from typing import Optional

from pydantic import BaseModel
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class VoucherLineCreate(BaseModel):
    account_id: int
    debit: Decimal = Field(default=0, ge=0)
    credit: Decimal = Field(default=0, ge=0)
    remarks: str | None = None


class VoucherCreate(BaseModel):
    voucher_date: date
    voucher_type: str
    narration: str | None = None
    lines: list[VoucherLineCreate]


class VoucherLineResponse(BaseModel):
    id: int
    account_id: int
    debit: Decimal
    credit: Decimal
    remarks: str | None = None

    model_config = {
        "from_attributes": True
    }


class VoucherResponse(BaseModel):
    id: int
    voucher_no: str
    voucher_date: date
    voucher_type: str
    narration: str | None = None

    lines: list[VoucherLineResponse]

    model_config = {
        "from_attributes": True
    }

class ChartOfAccountCreate(BaseModel):
    account_code: str
    account_name: str
    account_type: str
    account_group: str
    parent_id: Optional[int] = None
    opening_balance: float = 0
    balance_type: str
    is_active: bool = True


class ChartOfAccountResponse(BaseModel):
    id: int
    account_code: str
    account_name: str
    account_type: str
    account_group: str
    parent_id: Optional[int]
    opening_balance: float
    balance_type: str
    is_active: bool
    created_by: int

    class Config:
        from_attributes = True