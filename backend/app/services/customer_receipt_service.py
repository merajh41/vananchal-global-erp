from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.customer_receipt import CustomerReceipt
from app.models.user import User

from app.schemas.customer_receipt import CustomerReceiptCreate


class CustomerReceiptService:

    @staticmethod
    def create_receipt(
        db: Session,
        receipt: CustomerReceiptCreate,
        current_user: User,
    ):
        customer = (
            db.query(Customer)
            .filter(Customer.id == receipt.customer_id)
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found",
            )

        db_receipt = CustomerReceipt(
            customer_id=receipt.customer_id,
            receipt_date=receipt.receipt_date,
            amount=receipt.amount,
            payment_mode=receipt.payment_mode,
            reference_no=receipt.reference_no,
            remarks=receipt.remarks,
            created_by=current_user.id,
        )

        db.add(db_receipt)
        db.commit()
        db.refresh(db_receipt)

        return db_receipt