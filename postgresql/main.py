from contextlib import asynccontextmanager

from fastapi import FastAPI
from httpx import Request
from scalar_fastapi import get_scalar_api_reference
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response

from api.router import master_router
from database.session import create_db_tables



"""
Delivery Management System

## Seller

## Delivery

## Shipment


"""
class AppException(Exception):
    pass


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()
    yield


# FastAPI App
app = FastAPI(
    # Server start/stop listener
    lifespan=lifespan_handler,
    docs_url="/swagger",
    terms_of_service="https://google.com",
    contact={
        "name":"Shivam"
    }
)

app.include_router(master_router)


@app.exception_handler(AppException)
def handler(request: Request, exception: Exception):
    raise JSONResponse(
        content={"error": str(exception)},
        status_code=request.status_code,
    )


@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    response: Response = await call_next(request)

    # add_log()
    return response


app.add_middleware(CORSMiddleware,
                   allow_origins=["http:localhost:5500"],
                   allow_methods=["*"],
                   )


### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
