from fastapi import APIRouter
from models.models import Shipment, Seller
from models.schemas import SellerRead, SellerCreate
from ..dependencies.dependency import SellerServiceDepends

seller_router = APIRouter(prefix="/api/v1/seller", tags=["Seller"])


@seller_router.post("/signUp",response_model=SellerRead)
async def sign_up_seller(seller: SellerCreate,seller_service: SellerServiceDepends)-> Seller:

    seller = await seller_service.sign_up(seller)

    return seller