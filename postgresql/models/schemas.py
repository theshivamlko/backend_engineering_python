from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

from models.models import ShipmentStatus


class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25)
    destination: int


class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    estimated_delivery: datetime


class ShipmentCreate(BaseShipment):
    pass
    

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)


class SellerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class SellerRead(BaseModel):
    id: int
    name: str
    email: EmailStr
