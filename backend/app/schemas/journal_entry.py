from datetime import date
from typing import Optional

from pydantic import BaseModel


class JournalEntryCreate(BaseModel):
    entry_date: date
    account: str
    debit: float
    credit: float
    narration: Optional[str] = None
    reference_no: Optional[str] = None


class JournalEntryResponse(BaseModel):
    id: int
    entry_date: date
    account: str
    debit: float
    credit: float
    narration: Optional[str]
    reference_no: Optional[str]
    created_by: int

    class Config:
        from_attributes = True