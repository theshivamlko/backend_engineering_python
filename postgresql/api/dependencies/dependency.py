from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.session import get_session
from services.shipment_service import ShipmentService
from services.seller_service import SellerService
from services.delivery_partner_service import DeliveryPartnerService
from core.security import oauth_scheme, delivery_oauth_scheme
from utils import decode_access_token
from database.models.models import Seller, DeliveryPartner
from database.redis_db import is_jti_blacklisted

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def _get_access_token(token:str):

    data = decode_access_token(token)
    print("==>Decoded token data in get_access_token_service:", data["jti"])  # Debugging line

    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials")


    return data

async def get_access_token_seller(token: Annotated[str, Depends(oauth_scheme)]) -> dict:
    return await _get_access_token(token)

async def get_access_token_delivery_partner(token: Annotated[str, Depends(delivery_oauth_scheme)]) -> dict:
    return await _get_access_token(token)


async def get_current_seller(token_data: Annotated[dict, Depends(get_access_token_seller)], session: SessionDep):

    print("==>Token Data get_current_seller:", token_data)  # Debugging line

    if "id" in token_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    user_id = token_data["data"]["user"]["id"]
    print("==>get_current_user user_id:", user_id)  # Debugging line
    user = await session.get(Seller, UUID(user_id))
    print("==>get_current_user user:", user)  # Debugging line

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")

    return user


async def get_current_delivery_partner(token_data: Annotated[dict, Depends(get_access_token_delivery_partner)], session: SessionDep):

    print("==>Token Data get_current_delivery_partner:", token_data)  # Debugging line

    if "id" in token_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    user_id = token_data["data"]["user"]["id"]
    print("==>get_current_delivery_partner user_id:", user_id)  # Debugging line
    user = await session.get(DeliveryPartner, UUID(user_id))
    print("==>get_current_delivery_partner user:", user)  # Debugging line

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery partner not found")

    return user


def get_shipment_service(session: SessionDep) -> ShipmentService:
    return ShipmentService(session,DeliveryPartnerService(session))


def get_seller_service(session: SessionDep,) -> SellerService:
    return SellerService(session)

def get_delivery_partner_service(session: SessionDep) -> DeliveryPartnerService:
    return DeliveryPartnerService(session)


DeliveryPartnerDepends = Annotated[DeliveryPartner,Depends(get_current_delivery_partner)]

DeliveryPartnerAccessTokenDepends = Annotated[dict, Depends(get_access_token_delivery_partner)]

DeliveryPartnerServiceDepends = Annotated[DeliveryPartnerService,Depends(get_delivery_partner_service)]



SellerServiceDepends = Annotated[SellerService,Depends(get_seller_service)]

SellerDepends = Annotated[Seller,Depends(get_current_seller)]

SellerAccessTokenDepends = Annotated[dict, Depends(get_access_token_seller)]

ShipmentServiceDepends = Annotated[ShipmentService,Depends(get_shipment_service)]

