from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.session import get_session
from services.shipment import ShipmentService
from services.seller_service import SellerService
from core.security import oauth_scheme
from utils import decode_access_token
from models.models import Seller

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_access_token_service(token: Annotated[str, Depends(oauth_scheme)]):

    data = decode_access_token(token)

    if data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials")

    return data

async def get_current_user(token_data: Annotated[dict, Depends(get_access_token_service)], session: SessionDep):

    if "id" in token_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    print("Token Data get_current_user:", token_data)  # Debugging line
    user_id = token_data["data"]["user"]["id"]
    user = await session.get(Seller, user_id)

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