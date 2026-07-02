from pydantic import BaseModel, EmailStr


class CompanyCreate(BaseModel):
    name: str
    owner: str | None = None
    gst: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None


class CompanyResponse(CompanyCreate):
    id: int

    class Config:
        from_attributes = True