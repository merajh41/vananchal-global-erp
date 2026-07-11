from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.roles import require_role
from app.database.connection import get_db

from app.models.user import User

from app.schemas.journal_entry import (
    JournalEntryCreate,
    JournalEntryResponse,
)

from app.services.journal_entry_service import (
    JournalEntryService,
)


router = APIRouter(
    prefix="/journal-entries",
    tags=["Journal Entries"],
)


@router.post(
    "/",
    response_model=JournalEntryResponse,
)
def create_journal_entry(
    journal: JournalEntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return JournalEntryService.create(
        db=db,
        journal=journal,
        current_user=current_user,
    )


@router.get(
    "/",
    response_model=list[JournalEntryResponse],
)
def get_journal_entries(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    return JournalEntryService.get_all(db)