from functools import lru_cache

import httpx
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import settings

security = HTTPBearer()

SUPABASE_ISSUER = f"https://{settings.SUPABASE_PROJECT_ID}.supabase.co/auth/v1"
JWKS_URL = f"{SUPABASE_ISSUER}/.well-known/jwks.json"
AUDIENCE = "authenticated"


@lru_cache()
def get_jwks():
    response = httpx.get(JWKS_URL, timeout=5.0)
    response.raise_for_status()
    return response.json()


def verify_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        jwks = get_jwks()
        key = next(k for k in jwks["keys"] if k["kid"] == kid)

        public_key = jwt.algorithms.ECAlgorithm.from_jwk(key)

        payload = jwt.decode(
            token,
            public_key,
            algorithms=[settings.ALGORITHM],
            audience=AUDIENCE,
            issuer=SUPABASE_ISSUER,
        )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError as err:
        print(err)
        raise HTTPException(status_code=401, detail="Invalid token")
