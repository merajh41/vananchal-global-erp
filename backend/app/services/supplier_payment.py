from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.supplier import Supplier
from app.models.user import User
from app.models.supplier_payment import SupplierPayment

from app.schemas.supplier_payment import SupplierPaymentCreate


class SupplierPaymentService:

    @staticmethod
    def create_payment(
        db: Session,
        payment: SupplierPaymentCreate,
        current_user: User,
    ):

        supplier = (
            db.query(Supplier)
            .filter(Supplier.id == payment.supplier_id)
            .first()
        )

        if not supplier:
            raise HTTPException(
                status_code=404,
                detail="Supplier not found"
            )

        db_payment = SupplierPayment(
            supplier_id=payment.supplier_id,
            payment_date=payment.payment_date,
            amount=payment.amount,
            payment_mode=payment.payment_mode,
            reference_no=payment.reference_no,
            remarks=payment.remarks,
            created_by=current_user.id,
        )

        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)

        return db_payment