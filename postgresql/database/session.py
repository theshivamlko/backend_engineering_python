from typing import Annotated

from fastapi import Depends
from sqlalchemy  import   create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from database.config import settings
from models.models import Shipment
from sqlmodel import SQLModel, Session
from sqlalchemy.ext.asyncio import async_sessionmaker
engine = create_async_engine(
    url= settings.POSTGRES_URL,
    echo = True,

)

async def create_db_tables():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session=async_sessionmaker(bind=engine,class_= AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session


