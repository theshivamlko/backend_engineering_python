from datetime import datetime, timedelta
from fastapi import HTTPException

import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, SQLModel
from starlette import status
from config import security_settings

from models.schemas import SellerCreate
from models.models import Seller
from utils import generate_access_token, decode_access_token


class SellerService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def sign_up(self, seller_create: SellerCreate, ) -> Seller:
        pass_hash = CryptContext(schemes="bcrypt", deprecated='auto').hash(seller_create.password)

        seller = Seller(
            name=seller_create.name,
            email=seller_create.email,
            pass_hash=pass_hash
        )

        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)

        return seller

    async def token(self, email: str, password: str) -> str:
        print("token Email :", email)  # Debugging line
        result = await self.session.execute(select(Seller).where(Seller.email == email))

        seller = result.scalar()

        if seller is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")

        isVerified = CryptContext(schemes="bcrypt", deprecated='auto').verify(password, seller.pass_hash)
        print("Password verification result:", isVerified)  # Debugging line
        if not isVerified:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        token = generate_access_token({
            "user": seller.model_dump(exclude={"pass_hash"})
        })
        return token


async def login_seller(self, email: str, password: str) -> Seller:
    seller = await self.session.execute(
        self.session.query(Seller).filter(Seller.email == email)
    )
    seller = seller.scalar_one_or_none()
    if not seller:
        raise ValueError("Invalid email or password")
    if not CryptContext(schemes="bcrypt", deprecated='auto').verify(password, seller.pass_hash):
        raise ValueError("Invalid email or password")
    return seller
