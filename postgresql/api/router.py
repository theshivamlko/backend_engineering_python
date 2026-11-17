from .routers.seller_router import seller_router
from .routers.shipment_router import shipment_router
from .routers.delivery_partner_router import delivery_router
from fastapi import APIRouter


master_router = APIRouter()

master_router.include_router(seller_router)
master_router.include_router(shipment_router)
master_router.include_router(delivery_router)