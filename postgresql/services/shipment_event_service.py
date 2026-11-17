from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.models import ShipmentStatus, Shipment, ShipmentEvent


class ShipmentEventService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, shipment: Shipment, location: int = None, status: ShipmentStatus = None,
                  description: str = None) -> ShipmentEvent:

        if not location:
            last_event = await  self.get_latest_event(shipment)
            location = last_event.location

        if not status:
            last_event = await  self.get_latest_event(shipment)
            status = last_event.status
        if not description:
            description = await  self._generate_description(status,location)

        new_event = ShipmentEvent(
            self,
            location=location,
            status=status,
            description=description,
            shipment_id=shipment.id

        )

        await self.session.add(new_event)

        await self.session.commit()
        await self.session.refresh(new_event)

        return new_event

    async def get_latest_event(self, shipment: Shipment):
        timeline = shipment.timeline
        timeline.sort(key=lambda item: item.created_at)
        return timeline[-1]

    async def _generate_description(self,status:ShipmentStatus,location:int):

        match status:
            case ShipmentStatus.placed:
                return "Assigned delivery partner"
            case ShipmentStatus.out_for_delivery:
                return "Shipment out for delivery"
            case ShipmentStatus.delivered:
                return "Successfully delivered"
            case _ :
                return f"Scanned at {location}"


