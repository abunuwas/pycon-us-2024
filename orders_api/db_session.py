import random
import uuid

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from orders_api.models import Base, Product, Order

engine = create_engine("sqlite:///pyconus.db")
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)


fixture_products = [
    {
        "name": "Microservice APIs by Jose Haro Peralta",
        "price": 50,
        "stock": 20,
        "min_loyalty_points": 100,
    },
    {
        "name": "Automating the Boring Stuff with Python by Al Sweigart",
        "price": 10,
        "stock": 10,
        "min_loyalty_points": 500,
    },
    {
        "name": "Hacking APIs by Corey Ball",
        "price": 50,
        "stock": 50,
        "min_loyalty_points": 120,
    },
    {
        "name": "Fluent Python by Luciano Ramalho",
        "price": 15,
        "stock": 20,
        "min_loyalty_points": 650,
    },
    {
        "name": "Microservices Patterns by Chris Richardson",
        "price": 25,
        "stock": 37,
        "min_loyalty_points": 700,
    },
]


fixtures_orders = [
    {
        "amount": 1,
        "status": "paid",
    },
    {
        "amount": 10,
        "status": "pending",
    },
    {
        "amount": 5,
        "status": "paid",
    },
    {
        "amount": 6,
        "status": "delivered",
    },
    {
        "amount": 2,
        "status": "paid",
    },
    {
        "amount": 3,
        "status": "paid",
    }
]

with session_maker() as session:
    if not list(session.scalars(select(Product))):
        products = [
            Product(**product_details)
            for product_details in fixture_products
        ]
        session.add_all(products)
        session.commit()

        product_ids = [product.id for product in products]

    else:
        product_ids = list(session.scalars(select(Product.id)))

    if not list(session.scalars(select(Order))):
        orders = [
            Order(
                **order_details,
                product_id=random.choice(product_ids),
                user_id=str(uuid.uuid4()),
            )
            for order_details in fixtures_orders
        ]
        session.add_all(orders)
        session.commit()
