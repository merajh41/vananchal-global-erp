from pydantic import BaseModel


class BankAccountCreate(BaseModel):
    bank_name: str
    account_name: str
    account_number: str
    ifsc_code: str
    opening_balance: float


class BankAccountResponse(BaseModel):
    id: int
    bank_name: str
    account_name: str
    account_number: str
    ifsc_code: str
    opening_balance: float
    current_balance: float
    created_by: int

    class Config:
        from_attributes = True