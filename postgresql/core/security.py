from typing import Any, Annotated

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from starlette import status
from starlette.requests import HTTPConnection
from utils import decode_access_token

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/seller/sellerLogin")
delivery_oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/delivery/login")


# Same as OAuth2PasswordBearer,
# Gets header from request and checks if it is a valid bearer token
class AccessTokenBearer(HTTPBearer):
    async def __call__(
            self, request: HTTPConnection
    ) -> dict :

        # request.headers["Authorization"]
        credentials = await super().__call__(request)
        token = credentials.credentials
        data = decode_access_token(token)

        if data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
            )
        return  data


access_token_bearer = AccessTokenBearer( )

Annotated[dict , Depends(access_token_bearer) ]


