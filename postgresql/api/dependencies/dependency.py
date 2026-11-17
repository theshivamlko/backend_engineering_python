from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.session import get_session
from services.shipment import ShipmentService
from services.seller_service import SellerService
from core.security import oauth_scheme
from utils import decode_access_token
from database.models.models import Seller
from database.redis_db import is_jti_blacklisted

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_access_token_service(token: Annotated[str, Depends(oauth_scheme)]):

    data = decode_access_token(token)
    print("==>Decoded token data in get_access_token_service:", data["jti"])  # Debugging line

    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials")


    return data

async def get_current_user(token_data: Annotated[dict, Depends(get_access_token_service)], session: SessionDep):

    print("==>Token Data get_current_user:", token_data)  # Debugging line

    if "id" in token_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    user_id = token_data["data"]["user"]["id"]
    print("==>get_current_user user_id:", user_id)  # Debugging line
    user = await session.get(Seller, UUID(user_id))
    print("==>get_current_user user:", user)  # Debugging line

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


def get_shipment_service(session: SessionDep) -> ShipmentService:
    return ShipmentService(session)


def get_seller_service(session: SessionDep) -> SellerService:
    return SellerService(session)


ShipmentServiceDepends = Annotated[ShipmentService,Depends(get_shipment_service)]

SellerServiceDepends = Annotated[SellerService,Depends(get_seller_service)]

SellerDepends = Annotated[Seller,Depends(get_current_user)]

AccessTokenDepends = Annotated[dict, Depends(get_access_token_service)]