import datetime

from pydantic import BaseModel, Field
from typing import Optional, List


class DailyReportCreate(BaseModel):
    date: str = Field(..., title="Report Date")
    total_income: int = Field(..., title="Total Income")
    table_income: int = Field(..., title="Table Income")
    products: Optional[List] = Field(None, title="Products")
    product_income: int = Field(..., title="Product Income")
    total_play_time: int = Field(..., title="Total Play Time")


class DailyReportResponse(DailyReportCreate):
    id: int = Field(..., title="Report ID")
    created_at: datetime.datetime = Field(..., title="Created At")
    updated_at: datetime.datetime = Field(..., title="Updated At")

    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "date": "2021-08-06",
                "total_income": 1000,
                "table_income": 800,
                "product_income": 200,
                "total_play_time": 60,
                "created_at": "2021-08-06T12:00:00",
                "updated_at": "2021-08-06T12:00:00"
            }
        }


class TableReportCreate(BaseModel):
    table_id: int = Field(..., title="Table ID")
    total_income: int = Field(..., title="Total Income")
    total_play_time: int = Field(..., title="Total Play Time")


class TableReportResponse(TableReportCreate):
    id: int = Field(..., title="Report ID")
    created_at: datetime.datetime = Field(..., title="Created At")
    updated_at: datetime.datetime = Field(..., title="Updated At")

    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "table_id": 1,
                "total_income": 800,
                "total_play_time": 60,
                "created_at": "2021-08-06T12:00:00",
                "updated_at": "2021-08-06T12:00:00"
            }
        }
