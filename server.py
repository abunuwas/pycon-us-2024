from fastapi import FastAPI

from auth.auth_api import auth_router
from orders_api.internal_api import internal_api
from orders_api.orders import orders_api

server = FastAPI()

server.include_router(auth_router)
server.include_router(internal_api)
server.include_router(orders_api)
