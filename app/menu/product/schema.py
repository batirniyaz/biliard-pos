import datetime

from pydantic import BaseModel, Field
from typing import Optional, List

from app.menu.option.schema import OptionResponse


class ProductBase(BaseModel):
    name: str = Field(..., description="The name of the product")
    price: Optional[int] = Field(..., description="The price of the product")
    description: Optional[str] = Field(None, description="The description of the product")
    status: bool = Field(True, description="The status of the product")
    sort_order: int = Field(0, description="The sort order of the product")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Optional[str] = Field(None, description="The name of the product")
    price: Optional[int] = Field(None, description="The price of the product")
    description: Optional[str] = Field(None, description="The description of the product")
    status: Optional[bool] = Field(None, description="The status of the product")
    sort_order: Optional[int] = Field(None, description="The sort order of the product")


class ProductResponse(ProductBase):
    id: int = Field(..., description="The ID of the product")
    image: Optional[str] = Field(None, description="The image URL of the product")
    options: Optional[List[OptionResponse]] = Field(None, description="The options of the product")

    created_at: datetime.datetime = Field(..., description="The time the product was created")
    updated_at: datetime.datetime = Field(..., description="The time the product was updated")

    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Kebab",
                "price": 100.0,
                "description": "Go'sh, pomidor, qazi, so'siskali",
                "status": True,
                "sort_order": 1,
                "sub_category_id": 1,
                "image": "http://example.com/image.jpg",
                "options": [{"id": 1, "name": "6 person"}],
                "created_at": "2022-01-01T12:00:00",
                "updated_at": "2022-01-01T12:00:00"
            }
        }
