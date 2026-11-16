from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_session
from services.shipment import ShipmentService
from services.seller_service import SellerService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_shipment_service(session: SessionDep) -> ShipmentService:
    return ShipmentService(session)


def get_seller_service(session: SessionDep) -> SellerService:
    return SellerService(session)


ShipmentServiceDepends = Annotated[ShipmentService,Depends(get_shipment_service)]

SellerServiceDepends = Annotated[SellerService,Depends(get_seller_service)]