from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.constants.chart_of_accounts import ACCOUNT_TYPES

from app.models.chart_of_account import ChartOfAccount
from app.models.user import User
from app.models.voucher import Voucher
from app.models.voucher_line import VoucherLine

from app.schemas.accounting import (
    ChartOfAccountCreate,
    VoucherCreate,
)


class AccountingService:

    @staticmethod
    def create_voucher(
        db: Session,
        voucher: VoucherCreate,
        current_user: User,
    ):
        valid_types = {
            "PAYMENT",
            "RECEIPT",
            "CONTRA",
            "JOURNAL",
        }

        if voucher.voucher_type.upper() not in valid_types:
            raise HTTPException(
                status_code=400,
                detail="Invalid voucher type.",
            )

        if len(voucher.lines) < 2:
            raise HTTPException(
                status_code=400,
                detail="A voucher must contain at least two lines.",
            )

        total_debit = sum(
            Decimal(line.debit)
            for line in voucher.lines
        )

        total_credit = sum(
            Decimal(line.credit)
            for line in voucher.lines
        )

        if total_debit != total_credit:
            raise HTTPException(
                status_code=400,
                detail="Total Debit must equal Total Credit.",
            )

        voucher_count = db.query(Voucher).count() + 1

        voucher_no = (
            f"{voucher.voucher_type[:2].upper()}"
            f"{voucher_count:06d}"
        )

        db_voucher = Voucher(
            voucher_no=voucher_no,
            voucher_date=voucher.voucher_date,
            voucher_type=voucher.voucher_type.upper(),
            narration=voucher.narration,
            created_by=current_user.id,
        )

        db.add(db_voucher)
        db.flush()

        for line in voucher.lines:
            db.add(
                VoucherLine(
                    voucher_id=db_voucher.id,
                    account_id=line.account_id,
                    debit=line.debit,
                    credit=line.credit,
                    remarks=line.remarks,
                )
            )

        db.commit()
        db.refresh(db_voucher)

        return db_voucher

    @staticmethod
    def create_chart_of_account(
        db: Session,
        account: ChartOfAccountCreate,
        current_user: User,
    ):

        existing = (
            db.query(ChartOfAccount)
            .filter(
                ChartOfAccount.account_code == account.account_code
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Account code already exists.",
            )

        if account.balance_type not in ["Debit", "Credit"]:
            raise HTTPException(
                status_code=400,
                detail="Balance type must be Debit or Credit.",
            )

        if account.account_type not in ACCOUNT_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Invalid account type.",
            )

        if account.account_group not in ACCOUNT_TYPES[account.account_type]:
            raise HTTPException(
                status_code=400,
                detail="Invalid account group.",
            )

        if account.parent_id is not None:

            parent = (
                db.query(ChartOfAccount)
                .filter(
                    ChartOfAccount.id == account.parent_id
                )
                .first()
            )

            if parent is None:
                raise HTTPException(
                    status_code=404,
                    detail="Parent account not found.",
                )

        db_account = ChartOfAccount(
            account_code=account.account_code,
            account_name=account.account_name,
            account_type=account.account_type,
            account_group=account.account_group,
            parent_id=account.parent_id,
            opening_balance=account.opening_balance,
            balance_type=account.balance_type,
            is_active=account.is_active,
            created_by=current_user.id,
        )

        db.add(db_account)
        db.commit()
        db.refresh(db_account)

        return db_account

    @staticmethod
    def get_chart_of_accounts(db: Session):

        return (
            db.query(ChartOfAccount)
            .order_by(
                ChartOfAccount.account_type,
                ChartOfAccount.account_group,
                ChartOfAccount.account_code,
            )
            .all()
        )