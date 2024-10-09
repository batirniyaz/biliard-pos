from pydantic import BaseModel, Field
from typing import Optional
import datetime

from app.table.schema import TableResponse


class OrderCreate(BaseModel):
    table_id: int = Field(..., description="The table ID of the order")
    status: bool = Field(True, description="The status of the order")


class OrderUpdate(BaseModel):
    products: Optional[list] = Field([], description="The products of the order")
    options: Optional[list] = Field([], description="The options of the product")
    status: Optional[bool] = Field(None, description="The status of the order")


class OrderResponse(BaseModel):
    id: int = Field(..., description="The ID of the order")
    table_id: int = Field(..., description="The table ID of the order")
    table_name: Optional[str] = Field(None, description="The name of the table")
    table_price: Optional[float] = Field(None, description="The price of the table")
    table_status: Optional[bool] = Field(None, description="The status of the table")
    start_time: Optional[str] = Field(None, description="The start time of the order")
    products: list = Field([], description="The products of the order")
    options: list = Field([], description="The options of the product")
    end_time: Optional[str] = Field(None, description="The end time of the order")
    duration: Optional[float] = Field(None, description="The duration of the order")
    table_income: Optional[float] = Field(None, description="The income of the table")
    products_income: Optional[float] = Field(None, description="The income of the products")
    total: Optional[float] = Field(None, description="The total price of the order")
    date: Optional[str] = Field(None, description="The date of the order")
    status: bool = Field(..., description="The status of the order")

    created_at: datetime.datetime = Field(..., description="The time the order was created")
    updated_at: datetime.datetime = Field(..., description="The time the order was updated")

    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "table_id": 1,
                "table_name": "Table 1",
                "table_price": 100.0,
                "table_status": False,
                "start_time": "12:00:00",
                "products": [{"id": 1, "name": "Kebab", "price": 100.0}],
                "options": [{"id": 1, "name": "6 person"}],
                "end_time": "13:00:00",
                "duration": 60,
                "total": 200.0,
                "date": "2022-01-01",
                "status": True,
                "created_at": "2022-01-01T12:00:00",
                "updated_at": "2022-01-01T12:00:00"
            }
        }
