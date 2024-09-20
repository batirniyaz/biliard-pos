import datetime

from pydantic import BaseModel, Field
from typing import Optional


class TableBase(BaseModel):
    name: str = Field(..., title="Table Name")
    price: int = Field(..., title="Table Price")
    status: bool = Field(..., title="Table Status")


class TableCreate(TableBase):
    pass


class TableUpdate(TableBase):
    name: Optional[str] = Field(None, title="Table Name")
    price: Optional[int] = Field(None, title="Table Price")
    status: Optional[bool] = Field(None, title="Table Status")


class TableResponse(TableBase):
    id: int = Field(..., title="Table ID")
    created_at: datetime.datetime = Field(..., title="Created At")
    updated_at: datetime.datetime = Field(..., title="Updated At")

    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Table 1",
                "status": True,
                "created_at": "2021-08-06T12:00:00",
                "updated_at": "2021-08-06T12:00:00"
            }
        }
