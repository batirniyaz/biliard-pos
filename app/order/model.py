import datetime

from typing import List

from sqlalchemy import Integer, String, JSON, Float, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.auth.database import Base


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False, primary_key=True)
    table_id: Mapped[int] = mapped_column(Integer, ForeignKey("table.id"), nullable=False)
    table_name: Mapped[str] = mapped_column(String(length=255), nullable=True)
    table_price: Mapped[float] = mapped_column(Float, nullable=True)
    table_status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    start_time: Mapped[str] = mapped_column(String(length=255), nullable=True)
    products: Mapped[List] = mapped_column(JSON, default=[])
    options: Mapped[List] = mapped_column(JSON, default=[])
    end_time: Mapped[str] = mapped_column(String(length=255), nullable=True)
    duration: Mapped[float] = mapped_column(Float, nullable=True)
    total: Mapped[float] = mapped_column(Float, nullable=True, default=0)
    date: Mapped[str] = mapped_column(String(length=255), nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

