import datetime
from typing import List

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, TIMESTAMP, JSON
from app.auth.database import Base


class DailyReport(Base):
    __tablename__ = "daily_report"

    id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False, primary_key=True)
    date: Mapped[str] = mapped_column(String(length=20), nullable=False)
    total_income: Mapped[int] = mapped_column(Integer, nullable=False)
    table_income: Mapped[int] = mapped_column(Integer, nullable=False)
    product_income: Mapped[int] = mapped_column(Integer, nullable=False)
    products: Mapped[List] = mapped_column(JSON, default=[])
    total_play_time: Mapped[int] = mapped_column(Integer, nullable=False)
    orders: Mapped[List] = mapped_column(JSON, default=[], nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))


class TableReport(Base):
    __tablename__ = "table_report"

    id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False, primary_key=True)
    date: Mapped[str] = mapped_column(String(length=20), nullable=True)
    table_id: Mapped[int] = mapped_column(Integer, nullable=False)
    table_name: Mapped[str] = mapped_column(String(length=255), nullable=True)
    products: Mapped[List] = mapped_column(JSON, default=[])
    table_income: Mapped[int] = mapped_column(Integer, nullable=True)
    products_income: Mapped[int] = mapped_column(Integer, nullable=True)
    total_income: Mapped[int] = mapped_column(Integer, nullable=False)
    total_play_time: Mapped[int] = mapped_column(Integer, nullable=False)
    orders: Mapped[List] = mapped_column(JSON, default=[])

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
