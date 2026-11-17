from fastapi import APIRouter, HTTPException
from rich import status

from api.dependencies.dependency import ShipmentServiceDepends,SellerDepends
from models.models import Shipment, Seller
from models.schemas import ShipmentRead, ShipmentUpdate, ShipmentCreate



shipment_router = APIRouter(prefix="/api/v1", tags=["Shipment"])


### Read a shipment by id
@shipment_router.get("/shipment", response_model=ShipmentRead)
async def get_shipment(id:int, shipment: ShipmentCreate, service: ShipmentServiceDepends) -> Shipment:
    # Check for shipment with given id
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment



### Create a new shipment with content and weight
@shipment_router.post("/shipmentCreate", response_model=None)
async def create_shipment(seller: SellerDepends,update_shipment: ShipmentCreate, service: ShipmentServiceDepends) -> Shipment:
    shipment = await service.add(update_shipment)

    return  shipment


### Update fields of a shipment
@shipment_router.patch("/shipmentUpdate", response_model=ShipmentRead)
async def update_shipment(id: int, shipment_update: ShipmentUpdate,  service: ShipmentServiceDepends) -> Shipment:
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    updated_shipment = await service.update(id,shipment_update)

    return updated_shipment

### Delete a shipment by id
@shipment_router.delete("/shipmentDelete")
async def delete_shipment(id: int, service: ShipmentServiceDepends) -> dict[str, str]:
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return await service.delete(id)

