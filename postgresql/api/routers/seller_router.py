from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.security import oauth_scheme
from database.models.schemas import SellerRead, SellerCreate
from database.models.models import Seller
from ..dependencies.dependency import SellerServiceDepends, SessionDep, SellerAccessTokenDepends
from utils import decode_access_token
from database.redis_db import add_jti_to_blacklist


seller_router = APIRouter(prefix="/api/v1/seller", tags=["Seller"])


@seller_router.post("/signUp", response_model=SellerRead)
async def sign_up_seller(seller: SellerCreate, seller_service: SellerServiceDepends):
    seller = await seller_service.sign_up(seller)

    return seller


@seller_router.post("/sellerLogin")
async def login_seller(form: Annotated[OAuth2PasswordRequestForm, Depends()],
                       seller_service: SellerServiceDepends):
    token = await seller_service.token(form.username, form.password)
    print("Login Token:", token)  # Print the token for debugging purposes

    return {"access_token": token, "token_type": "bearer"}


@seller_router.post("/dashboard")
async def dashboard(token: Annotated[str, Depends(oauth_scheme)], session: SessionDep):
    print("Dashboard Token:", token)  # Print the token for debugging purposes

    payload = decode_access_token(token)

    seller = await session.get(Seller, payload["data"]["user"]["id"])
    seller_copy= seller.model_dump(exclude={"pass_hash"})


    return {"message": "Welcome to the seller dashboard!", "data": seller_copy}



@seller_router.get("/logout")
async def logout(token: SellerAccessTokenDepends, session: SessionDep):

    print("Logout Token:", token)  # Print the token for debugging purposes
    await add_jti_to_blacklist(token["jti"])


    # Here you can implement the logic to invalidate the token if needed

    return {"message": "Successfully logged out"}
