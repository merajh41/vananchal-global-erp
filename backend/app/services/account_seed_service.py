from sqlalchemy.orm import Session

from app.constants.chart_of_accounts import ACCOUNT_TYPES
from app.models.chart_of_account import ChartOfAccount


class AccountSeedService:

    @staticmethod
    def seed_default_accounts(
        db: Session,
        created_by: int,
    ):

        code = 1000

        for account_type, groups in ACCOUNT_TYPES.items():

            for account_group, accounts in groups.items():

                for account_name in accounts:

                    exists = (
                        db.query(ChartOfAccount)
                        .filter(
                            ChartOfAccount.account_name == account_name
                        )
                        .first()
                    )

                    if exists:
                        continue

                    balance_type = (
                        "Debit"
                        if account_type in ["Asset", "Expense"]
                        else "Credit"
                    )

                    db.add(
                        ChartOfAccount(
                            account_code=str(code),
                            account_name=account_name,
                            account_type=account_type,
                            account_group=account_group,
                            opening_balance=0,
                            balance_type=balance_type,
                            is_active=True,
                            created_by=created_by,
                        )
                    )

                    code += 1

        db.commit()