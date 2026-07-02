from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    username: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True