from .routers.seller import seller_router
from .routers.shipment import shipment_router
from fastapi import APIRouter


master_router = APIRouter()

master_router.include_router(seller_router)
master_router.include_router(shipment_router)