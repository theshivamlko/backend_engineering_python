from datetime import timedelta, timezone

from fastapi import HTTPException
from starlette import status

from config import security_settings


def generate_access_token(data: dict, expires_delta: timedelta = timedelta(seconds=15)) -> str:
    """
    Generate a JWT access token for the given user ID.

    :param data: The data to include in the token.
    :param user_id: The user ID for which to generate the token.
    :param secret_key: The secret key used to sign the token.
    :param algorithm: The algorithm used to sign the token.
    :param expires_delta: The expiration time in seconds for the token.
    :return: A JWT access token as a string.
    """
    from datetime import datetime
    import jwt

    expiration = datetime.now(timezone.utc) + expires_delta
    payload = {
        "data": data,
        "exp": expiration
    }
    print("Generating token with payload:", payload)  # Debugging line
    try:
        token = jwt.encode(payload=payload, key=security_settings.JWT_SECRET_KEY, algorithm=security_settings.JWT_ALGORITHM)
        return token
    except Exception as e:
        print("Error generating token:", e)  # Debugging line
        raise


def decode_access_token(token: str) -> dict:
    """
    Decode a JWT access token and return its payload.

    :param token: The JWT access token to decode.
    :return: The decoded payload as a dictionary.
    :raises jwt.ExpiredSignatureError: If the token has expired.
    :raises jwt.InvalidTokenError: If the token is invalid.
    """
    import jwt

    try:
        payload = jwt.decode(jwt=token, key=security_settings.JWT_SECRET_KEY, algorithms=[security_settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )
    except jwt.PyJWTError:
        raise None
