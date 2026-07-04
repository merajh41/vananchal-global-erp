from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    name: str
    mobile: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    gst_number: str | None = None


class CustomerResponse(CustomerCreate):
    id: int

    class Config:
        from_attributes = True