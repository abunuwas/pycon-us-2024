from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from orders_api.db_session import session_maker
from orders_api.models import Order

internal_api = APIRouter()


@internal_api.delete("/admin/orders/{order_id}", include_in_schema=False)
def admin_delete_order(order_id: UUID):
    with session_maker() as session:
        order = session.scalar(select(Order).where(Order.id == order_id))
        if order is None:
            raise HTTPException(
                status_code=404, detail=f"Order with ID {order_id} not found"
            )
        session.delete(order)
        session.commit()


@internal_api.get("/secrets", include_in_schema=False)
def leak_secrets():
    return "super secret!"
