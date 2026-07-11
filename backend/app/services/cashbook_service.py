from datetime import date

from sqlalchemy.orm import Session

from app.models.customer_receipt import CustomerReceipt
from app.models.expense import Expense
from app.models.income import Income
from app.models.supplier_payment import SupplierPayment


class CashBookService:

    @staticmethod
    def get_cashbook(
        db: Session,
        from_date: date,
        to_date: date,
    ):

        entries = []

        incomes = (
            db.query(Income)
            .filter(
                Income.expense_date if False else True
            )
        )

        incomes = (
            db.query(Income)
            .filter(
                Income.income_date >= from_date,
                Income.income_date <= to_date,
            )
            .all()
        )

        for item in incomes:
            entries.append({
                "date": item.income_date,
                "type": "Income",
                "description": item.category,
                "receipt": item.amount,
                "payment": 0,
            })

        receipts = (
            db.query(CustomerReceipt)
            .filter(
                CustomerReceipt.receipt_date >= from_date,
                CustomerReceipt.receipt_date <= to_date,
            )
            .all()
        )

        for item in receipts:
            entries.append({
                "date": item.receipt_date,
                "type": "Customer Receipt",
                "description": f"Customer #{item.customer_id}",
                "receipt": item.amount,
                "payment": 0,
            })

        expenses = (
            db.query(Expense)
            .filter(
                Expense.expense_date >= from_date,
                Expense.expense_date <= to_date,
            )
            .all()
        )

        for item in expenses:
            entries.append({
                "date": item.expense_date,
                "type": "Expense",
                "description": item.category,
                "receipt": 0,
                "payment": item.amount,
            })

        supplier_payments = (
            db.query(SupplierPayment)
            .filter(
                SupplierPayment.payment_date >= from_date,
                SupplierPayment.payment_date <= to_date,
            )
            .all()
        )

        for item in supplier_payments:
            entries.append({
                "date": item.payment_date,
                "type": "Supplier Payment",
                "description": f"Supplier #{item.supplier_id}",
                "receipt": 0,
                "payment": item.amount,
            })

        entries.sort(key=lambda x: x["date"])

        balance = 0

        for row in entries:
            balance += row["receipt"]
            balance -= row["payment"]
            row["balance"] = balance

        return entries