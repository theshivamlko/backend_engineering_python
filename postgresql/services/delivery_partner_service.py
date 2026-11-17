from collections.abc import Sequence

from fastapi import HTTPException

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, any_
from starlette import status

from database.models.schemas import DeliveryPartnerCreate, DeliveryPartnerUpdate
from database.models.models import DeliveryPartner, Shipment
from utils import generate_access_token


class DeliveryPartnerService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def sign_up(self, delivery_partner_create: DeliveryPartnerCreate,) -> DeliveryPartner:
        pass_hash = CryptContext(schemes="bcrypt", deprecated='auto').hash(delivery_partner_create.pass_hash)

        print("==> DeliveryPartnerService sign_up",delivery_partner_create)
        try:
            delivery_partner = DeliveryPartner(
                name=delivery_partner_create.name,
                email=delivery_partner_create.email,
                serviceable_zip_codes=delivery_partner_create.serviceable_area_code,
                max_handling_capacity=delivery_partner_create.max_handling_capacity,
                address=delivery_partner_create.address,
                pass_hash=pass_hash
            )


            self.session.add(delivery_partner)
            await self.session.commit()
            await self.session.refresh(delivery_partner)

            return delivery_partner
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def token(self, email: str, password: str) -> str:
        print("token Email :", email)  # Debugging line
        result = await self.session.execute(select(DeliveryPartner).where(DeliveryPartner.email == email))

        delivery_partner = result.scalar()

        if delivery_partner is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DeliveryPartner not found")

        isVerified = CryptContext(schemes="bcrypt", deprecated='auto').verify(password, delivery_partner.pass_hash)
        print("Password verification result:", isVerified)  # Debugging line
        if not isVerified:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        token = generate_access_token({
            "user": delivery_partner.model_dump(mode="json", exclude={"pass_hash"})
        })
        return token

    async def login_delivery_partner(self, email: str, password: str) -> DeliveryPartner:
        delivery_partner = await self.session.execute(
            self.session.query(DeliveryPartner).filter(DeliveryPartner.email == email)
        )
        delivery_partner = delivery_partner.scalar_one_or_none()
        if not delivery_partner:
            raise ValueError("Invalid email or password")
        if not CryptContext(schemes="bcrypt", deprecated='auto').verify(password, DeliveryPartner.pass_hash):
            raise ValueError("Invalid email or password")
        return delivery_partner

    async def update(self, id: int, delivery_partner_update: DeliveryPartnerUpdate) -> DeliveryPartner:

        if not delivery_partner_update:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided to update",
            )

        delivery_partner = await self.get(id)
        delivery_partner.sqlmodel_update(delivery_partner_update)

        self.session.add(delivery_partner)
        await self.session.commit()
        await self.session.refresh(delivery_partner)

        return delivery_partner

    async def get_partner_by_zipcodes(self, zipcode: int, ) -> Sequence[DeliveryPartner]:

        result = await self.session.execute(
            select(DeliveryPartner).where(any_(DeliveryPartner.serviceable_zip_codes) == zipcode)
        )

        delivery_partner = result.scalar()

        if not delivery_partner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Delivery partner not found for the given zipcode"
            )
        return delivery_partner

    async def assign_shipment_to_partner(self, shipment: Shipment):
        delivery_partners = await self.get_partner_by_zipcodes(shipment.destination)

        if not delivery_partners:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Delivery partner not found"
            )

        for partner in delivery_partners:
            if partner.current_handling_capacity > 0:
                partner.shipments.append(shipment)

                return shipment

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No delivery partner available !"
        )
