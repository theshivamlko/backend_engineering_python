from datetime import datetime, timezone, timedelta
from uuid import UUID

from fastapi import HTTPException
from rich import status
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.models import Shipment, ShipmentStatus, Seller, DeliveryPartner
from database.models.schemas import ShipmentUpdate
from services.delivery_partner_service import DeliveryPartnerService
from services.shipment_event_service import ShipmentEventService


class ShipmentService:
    def __init__(self, session: AsyncSession, delivery_partner_service: DeliveryPartnerService,
                 event_service: ShipmentEventService) -> None:
        self.session = session
        self.delivery_partner_service = delivery_partner_service
        self.event_service = event_service

    async def get(self, id: UUID) -> Shipment | None:
        return await self.session.get(Shipment, id)

    async def add(self, shipment: Shipment, seller: Seller) -> Shipment:
        new_shipment = Shipment(
            **shipment.model_dump(mode="json"),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now(tz=timezone.utc) + timedelta(days=3),
            seller_id=seller.id,
            seller=seller
        )

        partner = await self.delivery_partner_service.assign_shipment_to_partner(new_shipment)

        new_shipment.delivery_partner_id = partner.id

        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)

        await self.event_service.add(shipment=new_shipment, location=seller.zip_code, status=ShipmentStatus.placed,
                                     description=f"Assigned to partner")

        return new_shipment

    async def update(self, id: UUID, shipment_update: ShipmentUpdate,partner:DeliveryPartner) -> Shipment:

        shipment = await self.get(id)

        if shipment.delivery_partner_id != partner.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not authorized",
            )

        if shipment_update.estimated_delivery:
            shipment.estimated_delivery = shipment_update.estimated_delivery

        shipment.sqlmodel_update(shipment_update)



        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

        return shipment

    async def delete(self, id: UUID) -> dict[str, str]:
        shipment = await self.get(id)
        await self.session.delete(shipment)
        await self.session.commit()

        return {"detail": f"Shipment with id #{id} is deleted!"}
