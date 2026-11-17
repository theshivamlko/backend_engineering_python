from uuid import UUID

from fastapi import APIRouter, HTTPException
from rich import status

from api.dependencies.dependency import ShipmentServiceDepends, SellerDepends, DeliveryPartnerDepends
from database.models.models import Shipment
from database.models.schemas import ShipmentRead, ShipmentUpdate, ShipmentCreate
from utils import parse_shipment_id



shipment_router = APIRouter(prefix="/api/v1", tags=["Shipment"])


### Read a shipment by id
@shipment_router.get("/shipment", response_model=ShipmentRead)
async def get_shipment(id:UUID, seller: SellerDepends, service: ShipmentServiceDepends) -> Shipment:
    # Check for shipment with given id
    print(f"==>Getting shipment with id: {id}")
    # uuid = parse_shipment_id(id)
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment


### Create a new shipment with content and weight
@shipment_router.post("/shipmentCreate", response_model=None)
async def create_shipment(update_shipment: ShipmentCreate, seller: SellerDepends, service: ShipmentServiceDepends) -> Shipment:


    shipment = await service.add(update_shipment,seller)


    return  shipment


### Update fields of a shipment
@shipment_router.patch("/shipmentUpdate", response_model=ShipmentRead)
async def update_shipment(id: UUID, shipment_update: ShipmentUpdate,
                          partner: DeliveryPartnerDepends,
                          service: ShipmentServiceDepends) -> Shipment:
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
async def delete_shipment(id: UUID,  service: ShipmentServiceDepends) -> dict[str, str]:
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return await service.delete(id)

