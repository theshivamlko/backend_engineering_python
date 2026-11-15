from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_session
from services.shipment import ShipmentService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_shipment_service(session: SessionDep) -> ShipmentService:
    return ShipmentService(session)


ShipmentServiceDepends = Annotated[ShipmentService,Depends(get_shipment_service)]