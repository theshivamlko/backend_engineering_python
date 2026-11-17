from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, ConfigDict

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
    created_at: datetime


class DeliveryPartnerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: EmailStr
    serviceable_area_code: list[int] = Field(validation_alias="serviceable_zip_codes")
    max_handling_capacity:int


class DeliveryPartnerRead(DeliveryPartnerBase):
    id: UUID
    shipments: list[ShipmentRead] = []
    created_at: datetime


class DeliveryPartnerCreate(DeliveryPartnerBase):
    pass_hash: str
    address: str

class DeliveryPartnerUpdate(BaseModel):
    serviceable_area_code: list[int]
    max_handling_capacity: int

