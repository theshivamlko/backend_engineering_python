from datetime import datetime, timezone, timedelta
from uuid import UUID

from fastapi import HTTPException
from rich import status
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.models import Shipment, ShipmentStatus, Seller
from services.delivery_partner_service import DeliveryPartnerService


class ShipmentService:
    def __init__(self, session: AsyncSession, delivery_partner_service: DeliveryPartnerService) -> None:
        self.session = session
        self.delivery_partner_service = delivery_partner_service

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

        return new_shipment

    async def update(self, id: int, shipment_update: Shipment) -> Shipment:
        if not shipment_update:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided to update",
            )

        shipment = await self.get(id)
        shipment.sqlmodel_update(shipment_update)

        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

        return shipment

    async def delete(self, id: int) -> dict[str, str]:
        shipment = await self.get(id)
        await self.session.delete(shipment)
        await self.session.commit()

        return {"detail": f"Shipment with id #{id} is deleted!"}
