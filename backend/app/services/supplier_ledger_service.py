from sqlalchemy.orm import Session

from app.models.purchase import Purchase
from app.models.purchase_return import PurchaseReturn
from app.models.supplier_payment import SupplierPayment


class SupplierLedgerService:

    @staticmethod
    def supplier_ledger(
        db: Session,
        supplier_id: int,
    ):

        entries = []

        # Purchases (Debit)
        purchases = (
            db.query(Purchase)
            .filter(Purchase.supplier_id == supplier_id)
            .all()
        )

        for purchase in purchases:
            entries.append(
                {
                    "date": purchase.purchase_date,
                    "transaction_type": "Purchase",
                    "reference": purchase.invoice_no,
                    "debit": purchase.total_amount,
                    "credit": 0,
                }
            )

        # Purchase Returns (Credit)
        purchase_returns = (
            db.query(PurchaseReturn)
            .filter(PurchaseReturn.supplier_id == supplier_id)
            .all()
        )

        for pr in purchase_returns:
            entries.append(
                {
                    "date": pr.return_date,
                    "transaction_type": "Purchase Return",
                    "reference": pr.return_no,
                    "debit": 0,
                    "credit": pr.total_amount,
                }
            )

        # Supplier Payments (Credit)
        payments = (
            db.query(SupplierPayment)
            .filter(SupplierPayment.supplier_id == supplier_id)
            .all()
        )

        for payment in payments:
            entries.append(
                {
                    "date": payment.payment_date,
                    "transaction_type": "Payment",
                    "reference": payment.reference_no or f"PAY-{payment.id}",
                    "debit": 0,
                    "credit": payment.amount,
                }
            )

        # Sort by date
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

        total_purchase = sum(item["debit"] for item in entries)
        total_payment = sum(item["credit"] for item in entries)

        return {
            "supplier_id": supplier_id,
            "total_purchase": total_purchase,
            "total_payment": total_payment,
            "outstanding": balance,
            "ledger": ledger,
        }