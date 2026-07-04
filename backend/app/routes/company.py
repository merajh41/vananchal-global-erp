from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.company import Company
from app.models.user import User
from app.schemas.company import CompanyCreate, CompanyResponse

from app.auth.dependencies import get_current_user
from app.auth.roles import require_role

router = APIRouter(
    prefix="/company",
    tags=["Company"]
)


@router.post("/", response_model=CompanyResponse)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    db_company = Company(**company.model_dump())

    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company


@router.get("/")
def get_companies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Company).all()