import datetime

from sqlalchemy import Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.auth.database import Base


class Option(Base):
    __tablename__ = "option"

    id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True)
    price: Mapped[int] = mapped_column(Integer, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)

    product = relationship("Product", back_populates="options")

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
