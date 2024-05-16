import uuid
from datetime import datetime, timezone

from sqlalchemy import Uuid, DateTime, MetaData, create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s_idx",
            "uq": "uq_%(table_name)s_%(column_0_name)s_key",
            "ck": "ck_%(table_name)s_%(constraint_name)s_check",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s_fkey",
            "pk": "pk_%(table_name)s_pkey",
        }
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda _: datetime.now(timezone.utc)
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda _: datetime.now(timezone.utc)
    )


class Product(Base):
    __tablename__ = "product"

    name: Mapped[str]
    price: Mapped[float]
    stock: Mapped[int]
    min_loyalty_points: Mapped[int]


class Order(Base):
    __tablename__ = "order"

    user_id: Mapped[str]
    product_id: Mapped[Uuid] = mapped_column(ForeignKey("product.id"))
    amount: Mapped[int]
    status: Mapped[str]


Base.metadata.create_all(create_engine("sqlite:///pyconus.db"))
