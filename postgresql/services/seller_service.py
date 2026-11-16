from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import deprecated

from models.schemas import SellerCreate
from models.models import Seller



class SellerService:
    def __init__(self,session:AsyncSession ) -> None:
        self.session = session

    async def sign_up(self, seller_create: SellerCreate, ) -> Seller:

        pass_hash = CryptContext(schemes="bcrypt",deprecated='auto' ).hash(seller_create.password)

        seller = Seller(
            name=seller_create.name,
            email=seller_create.email,
            pass_hash=pass_hash
        )

        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)

        return seller