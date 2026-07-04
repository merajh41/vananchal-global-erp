from pydantic import BaseModel, EmailStr


class SupplierCreate(BaseModel):
    name: str
    contact_person: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    gst_number: str | None = None


class SupplierResponse(SupplierCreate):
    id: int

    class Config:
        from_attributes = True