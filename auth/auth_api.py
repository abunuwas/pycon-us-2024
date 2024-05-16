import os

import requests
from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import RedirectResponse

auth_router = APIRouter()

client_id = os.getenv("auth0_client_id")
client_secret = os.getenv("auth0_client_secret")
authorizer_url = os.getenv("auth0_domain")

assert client_id is not None, "auth0_client_id environment variable needed."
assert client_secret is not None, "auth0_client_secret environment variable needed."
assert authorizer_url is not None, "auth0_domain environment variable needed."


@auth_router.get("/login")
def login():
    url = (
        "https://pyconus.eu.auth0.com/authorize?"
        "response_type=code"
        "&audience=https://pycon-us-2024-api.com"
        f"&client_id={client_id}"
        "&redirect_uri=http://localhost:8000/docs"
    )
    return RedirectResponse(url)


class AuthCode(BaseModel):
    code: str


@auth_router.post("/token")
def get_auth_token(code: AuthCode):
    payload = (
        "grant_type=authorization_code"
        f"&client_id={client_id}"
        f"&client_secret={client_secret}"
        f"&code={code.code}"
        f"&redirect_uri=http://localhost:8000/docs"
    )
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(
        "https://pyconus.eu.auth0.com/oauth/token",
        data=payload,
        headers=headers,
    )
    return response.json()
