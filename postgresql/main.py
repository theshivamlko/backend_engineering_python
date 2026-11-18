from contextlib import asynccontextmanager

from fastapi import FastAPI
from httpx import Request
from scalar_fastapi import get_scalar_api_reference
from starlette.responses import JSONResponse

from api.router import master_router
from database.session import  create_db_tables


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
)

app.include_router(master_router)

@app.exception_handler(AppException)
def handler(request:Request,exception:Exception):
    raise JSONResponse(
        content={"error": str(exception)},
        status_code=request.status_code,
    )

### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
