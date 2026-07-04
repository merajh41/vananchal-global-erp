from pydantic import BaseModel


class WarehouseCreate(BaseModel):
    name: str
    address: str | None = None
    manager: str | None = None


class WarehouseResponse(BaseModel):
    id: int
    name: str
    address: str | None = None
    manager: str | None = None

    class Config:
        from_attributes = True