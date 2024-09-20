import datetime

from pydantic import BaseModel, Field
from typing import Optional


class OptionBase(BaseModel):
    name: str = Field(..., description="The name of the option")
    price: Optional[int] = Field(None, description="The price of the option")
    sort_order: int = Field(0, description="The sort order of the option")
    product_id: int = Field(..., description="The product ID of the option")


class OptionCreate(OptionBase):
    pass


class OptionUpdate(OptionBase):
    name: Optional[str] = Field(None, description="The name of the option")
    price: Optional[int] = Field(None, description="The price of the option")
    sort_order: Optional[int] = Field(None, description="The sort order of the option")
    product_id: Optional[int] = Field(None, description="The product ID of the option")


class OptionResponse(OptionBase):
    id: int = Field(..., description="The ID of the option")

    created_at: datetime.datetime = Field(..., description="The time the option was created")
    updated_at: datetime.datetime = Field(..., description="The time the option was updated")

    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "6 person",
                "price": 100.0,
                "sort_order": 1,
                "product_id": 1,
                "created_at": "2022-01-01T12:00:00",
                "updated_at": "2022-01-01T12:00:00"
            }
        }