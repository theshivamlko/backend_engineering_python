from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from database.models.schemas import DeliveryPartnerRead, DeliveryPartnerCreate, DeliveryPartnerUpdate
from ..dependencies.dependency import SessionDep, SellerAccessTokenDepends, \
    DeliveryPartnerAccessTokenDepends, DeliveryPartnerDepends, DeliveryPartnerServiceDepends
from database.redis_db import add_jti_to_blacklist


delivery_router = APIRouter(prefix="/api/v1/delivery", tags=["Delivery Partner"])


@delivery_router.post("/signUp", response_model=DeliveryPartnerRead)
async def sign_up_partner(delivery_partner_create: DeliveryPartnerCreate, delivery_partner_service: DeliveryPartnerServiceDepends):
    delivery_partner = await delivery_partner_service.sign_up(delivery_partner_create)

    return delivery_partner


@delivery_router.post("/login")
async def login_partner(form: Annotated[OAuth2PasswordRequestForm, Depends()],
                       delivery_partner_service: DeliveryPartnerServiceDepends):

    token = await delivery_partner_service.token(form.username, form.password)

    print("Login Token:", token)  # Print the token for debugging purposes

    return {"access_token": token, "token_type": "bearer"}


@delivery_router.post("/update")
async def update_delivery_partner(partner_update:DeliveryPartnerUpdate,
                                  partner:DeliveryPartnerDepends,
                        service: DeliveryPartnerServiceDepends):
    await service.update(partner.sqlmodel_update(partner_update))


@delivery_router.get("/logout")
async def logout(token: DeliveryPartnerAccessTokenDepends, session: SessionDep):

    print("Logout Token:", token)  # Print the token for debugging purposes
    await add_jti_to_blacklist(token["jti"])


    # Here you can implement the logic to invalidate the token if needed

    return {"message": "Successfully logged out"}
