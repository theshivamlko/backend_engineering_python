from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr

from database.models.models import ShipmentStatus, Seller


class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25)
    destination: int



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
    id: UUID
    name: str
    email: EmailStr


class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    estimated_delivery: datetime
    id: UUID
    seller:SellerRead
