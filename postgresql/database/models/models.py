from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlmodel import Field, SQLModel, Relationship


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


# Inherit SQLModel and set table = True
# to make a table in database
class Shipment(SQLModel, table=True):
    # Optional table name
    __tablename__ = "shipment"

    # Primary key with default value will be
    # assigned and incremented automatically
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default= uuid4,
            primary_key=True
        )
    )

    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime

    seller_id: UUID = Field(foreign_key="seller.id")
    seller: "Seller" = Relationship(back_populates="shipments",
                                    sa_relationship_kwargs={"lazy": "selectin"})


class Seller(SQLModel, table=True):
    __tablename__ = "seller"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True
        )
    )
    name: str
    email: str
    pass_hash: str
    shipments: list[Shipment] = Relationship(back_populates="seller",
                                             sa_relationship_kwargs={"lazy": "selectin"}
                                             )
