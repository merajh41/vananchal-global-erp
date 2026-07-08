from sqlalchemy.orm import Session

from app.models.sale import Sale
from app.models.customer_receipt import CustomerReceipt


class LedgerService:

    @staticmethod
    def customer_ledger(
        db: Session,
        customer_id: int,
    ):

        entries = []

        sales = (
            db.query(Sale)
            .filter(Sale.customer_id == customer_id)
            .all()
        )

        for sale in sales:
            entries.append(
                {
                    "date": sale.sale_date,
                    "transaction_type": "Sale",
                    "reference": sale.invoice_no,
                    "debit": sale.total_amount,
                    "credit": 0,
                }
            )

        receipts = (
            db.query(CustomerReceipt)
            .filter(CustomerReceipt.customer_id == customer_id)
            .all()
        )

        for receipt in receipts:
            entries.append(
                {
                    "date": receipt.receipt_date,
                    "transaction_type": "Receipt",
                    "reference": receipt.reference_no or f"REC-{receipt.id}",
                    "debit": 0,
                    "credit": receipt.amount,
                }
            )

        entries.sort(key=lambda x: x["date"])

        balance = 0
        ledger = []

        for entry in entries:

            balance += entry["debit"]
            balance -= entry["credit"]

            ledger.append(
                {
                    "date": entry["date"],
                    "transaction_type": entry["transaction_type"],
                    "reference": entry["reference"],
                    "debit": entry["debit"],
                    "credit": entry["credit"],
                    "balance": balance,
                }
            )

        total_sales = sum(item["debit"] for item in entries)
        total_receipts = sum(item["credit"] for item in entries)

        return {
            "customer_id": customer_id,
            "total_sales": total_sales,
            "total_receipts": total_receipts,
            "outstanding": balance,
            "ledger": ledger,
        }