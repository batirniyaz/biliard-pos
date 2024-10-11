from typing import Optional, Union

from fastapi import APIRouter, Depends, UploadFile, Form, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth.auth_backend import current_active_user
from app.auth.database import get_async_session, User

from app.menu.product.crud import create_product, get_products, get_product, update_product, delete_product
from app.menu.product.schema import ProductCreate, ProductUpdate, ProductResponse

from fastapi_cache.decorator import cache

router = APIRouter()


@router.post("/", response_model=ProductResponse)
async def create_product_endpoint(
        name: str = Form(...),
        price: Optional[float] = Form(None),
        description: str = Form(...),
        status: bool = Form(...),
        sort_order: int = Form(...),
        image: UploadFile = File(...),
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user.is_superuser:
        raise Exception("Only superuser can create product")

    product = ProductCreate(
        name=name,
        price=price,
        description=description,
        status=status,
        sort_order=sort_order,
    )

    return await create_product(db, product, image)


@router.get("/")
@cache(expire=60)
async def get_products_endpoint(
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await get_products(db)


@router.get("/{product_id}")
@cache(expire=60)
async def get_product_endpoint(
        product_id: int,
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await get_product(db, product_id)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product_endpoint(
        product_id: int,
        name: Optional[str] = Form(None),
        price: Optional[int] = Form(None),
        description: Optional[str] = Form(None),
        status: Optional[bool] = Form(None),
        sort_order: Optional[int] = Form(None),
        image: Union[Optional[UploadFile], str] = File(None),
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user.is_superuser:
        raise Exception("Only superuser can update product")
    product = ProductUpdate(
        name=name,
        price=price,
        description=description,
        status=status,
        sort_order=sort_order,
    )
    return await update_product(db, product_id, product, image)


@router.delete("/{product_id}")
async def delete_product_endpoint(
        product_id: int,
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user.is_superuser:
        raise Exception("Only superuser can delete product")
    return await delete_product(db, product_id)
