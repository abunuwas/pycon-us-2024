import os

import requests

from jose import jwt, jws, ExpiredSignatureError, JWTError
from jose.exceptions import JWTClaimsError, JWSError
from pydantic import BaseModel
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


authorizer_url = "https://pyconus.eu.auth0.com"

assert authorizer_url is not None, "authorizer environment variable is required."

jwks_endpoint = f"{authorizer_url}/.well-known/jwks.json"

jwks = requests.get(jwks_endpoint).json()["keys"]

AUTH_ON = os.getenv("AUTH_ON", "false") == "true"


def find_public_key(kid):
    for key in jwks:
        if key["kid"] == kid:
            return key


def validate_token(token):
    unverified_headers = jws.get_unverified_header(token)
    return jwt.decode(
        token=token,
        key=find_public_key(unverified_headers["kid"]),
        audience="https://pycon-us-2024-api.com",
        algorithms="RS256",
    )


class UserClaims(BaseModel):
    sub: str
    permissions: list[str]

    def is_admin(self):
        return "pentatonic:admin" in self.permissions


class AuthorizeRequestMiddleware(BaseHTTPMiddleware):
    def __init__(self, *args, **kwargs):
        super(AuthorizeRequestMiddleware, self).__init__(*args, **kwargs)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if not AUTH_ON:
            request.state.user = UserClaims(
                sub="110440199355640730133",
                permissions=["admin"],
            )
            return await call_next(request)
        if request.url.path in [
            "/health",
            "/docs",
            "/openapi.json",
            "/redocs",
            "/login",
            "/token",
            "/refresh-token",
        ]:
            return await call_next(request)
        if request.method == "OPTIONS":
            return await call_next(request)

        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Missing access token",
                    "body": "Missing access token",
                },
            )
        try:
            auth_token = bearer_token.split(" ")[1].strip()
            token_payload = validate_token(auth_token)
        except (
            ExpiredSignatureError,
            JWTError,
            JWTClaimsError,
            JWSError,
        ) as error:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": str(error), "body": str(error)},
            )
        else:
            request.state.user = UserClaims(
                sub=token_payload["sub"],
                permissions=token_payload.get("permissions", []),
            )
        return await call_next(request)
