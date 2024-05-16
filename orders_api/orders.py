import enum
import uuid
from datetime import datetime
from typing import Optional, Annotated
from uuid import UUID

import requests
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict
from pydantic_core import Url
from sqlalchemy import select, text
from starlette import status

from auth.auth_middleware import validate_token
from orders_api.db_session import session_maker
from orders_api.models import Product, Order

orders_api = APIRouter()


class ProductSchema(BaseModel):
    id: UUID
    name: str
    price: float
    stock: int
    min_loyalty_points: int


class ListProducts(BaseModel):
    products: list[ProductSchema]


class PlaceOrderSchema(BaseModel):
    model_config = ConfigDict(extra='allow')

    product_id: UUID
    amount: int


class OrderStatusEnum(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    delivered = "delivered"


class GetOrderSchema(PlaceOrderSchema):
    id: UUID
    user_id: str
    created: datetime
    status: OrderStatusEnum


class ListOrders(BaseModel):
    orders: list[GetOrderSchema]


security = HTTPBearer()


def authorize_access(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    return validate_token(credentials.credentials)


@orders_api.get("/products", response_model=ListProducts)
def list_products():
    with session_maker() as session:
        products = list(session.scalars(select(Product)))
        return {"products": products}


@orders_api.get("/orders", response_model=ListOrders)
def list_orders(
        user_claims: dict = Depends(authorize_access),
        status: Optional[str] = "paid"
):
    # BOLA
    # injection param: ' OR 1=1--
    with session_maker() as session:
        orders = session.execute(
            text(
                # f"select * from 'order' where status = '{status or ''}';"
                f"select * from 'order' where status = '{status or ''}'"
                f"and user_id = '{user_claims['sub']}';"
            )
        )
        return {"orders": orders}


@orders_api.post(
    "/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema,
)
def place_order(order_details: PlaceOrderSchema):
    with session_maker() as session:
        order = Order(
            product_id=order_details.product_id,
            amount=order_details.amount,
            user_id=str(uuid.uuid4()),
            status=OrderStatusEnum.pending.value,
        )
        session.add(order)
        session.commit()
        session.refresh(order)
        return order


@orders_api.get("/orders/{order_id}", response_model=GetOrderSchema)
def get_order_details(order_id: UUID):
    # anyone can see each other's orders
    with session_maker() as session:
        order = session.scalar(select(Order).where(Order.id == order_id))
        if order is not None:
            return order
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found"
        )


@orders_api.put("/orders/{order_id}", response_model=GetOrderSchema)
def update_order_details(order_id: UUID, order_details: PlaceOrderSchema):
    # mass assignment
    with session_maker() as session:
        order = session.scalar(select(Order).where(Order.id == order_id))

        if order is not None:
            for key, value in order_details:
                setattr(order, key, value)
            session.commit()
            session.refresh(order)
            return order

        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found"
        )


@orders_api.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
    with session_maker() as session:
        order = session.scalar(select(Order).where(Order.id == order_id))
        if order is None:
            raise HTTPException(
                status_code=404, detail=f"Order with ID {order_id} not found"
            )
        session.delete(order)
        session.commit()


@orders_api.get("/fetch-external-data")
def fetch_external_data(url: Url):
    # ssrf
    return requests.get(url).content
