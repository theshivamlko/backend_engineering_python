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

    delivery_partner_id: UUID = Field(foreign_key="delivery_partner.id")
    delivery_partner: "DeliveryPartner" = Relationship(back_populates="shipments")
    created_at: datetime = Field(sa_column=Column(
        postgresql.TIMESTAMP(timezone=False),
        default=datetime.utcnow,
        nullable=False
    ))


class User(SQLModel):

    name: str
    email: str
    address: str
    pass_hash: str

class Seller(User, table=True):
    __tablename__ = "seller"
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True
        )
    )
    created_at: datetime = Field(sa_column=Column(
        postgresql.TIMESTAMP(timezone=False),
        default=datetime.utcnow,
        nullable=False
    ))

    address: str
    shipments: list[Shipment] = Relationship(back_populates="seller",
                                             sa_relationship_kwargs={"lazy": "selectin"}
                                             )


class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partner"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True
        )
    )
    created_at: datetime = Field(sa_column=Column(
        postgresql.TIMESTAMP(timezone=False),
        default=datetime.utcnow,
        nullable=False
    ))
    serviceable_zip_codes: list[int] = Field(sa_column=Column(postgresql.ARRAY(postgresql.INTEGER)))
    max_handling_capacity: int
    shipments: list[Shipment] = Relationship(back_populates="delivery_partner",
                                              sa_relationship_kwargs={"lazy": "selectin"}

                                              )

    @property
    def active_shipments(self):
       return [
            shipment for shipment in self.shipments if shipment.status == ShipmentStatus.delivered
        ]

    @property
    def current_handling_capacity(self):
        return self.max_handling_capacity - len(self.active_shipments)