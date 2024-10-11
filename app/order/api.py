from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth_backend import current_active_user
from app.auth.database import get_async_session, User

from app.order.schema import OrderCreate, OrderResponse, OrderUpdate
from app.order.crud import create_order, update_order, get_order, get_orders, delete_order, get_all_orders, cancel_order

router = APIRouter()


@router.post("/", response_model=OrderResponse)
async def create_order_endpoint(
        order: OrderCreate,
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await create_order(db, order)


@router.get("/all", response_model=List[OrderResponse])
@cache(expire=60)
async def get_all_orders_endpoint(
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await get_all_orders(db)


@router.get("/", response_model=List[OrderResponse])
@cache(expire=60)
async def get_orders_endpoint(
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await get_orders(db)


@router.get("/{order_id}", response_model=OrderResponse)
@cache(expire=60)
async def get_order_endpoint(
        order_id: int,
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await get_order(db, order_id)


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order_endpoint(
        order_id: int,
        order: OrderUpdate,
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await update_order(db, order_id, order)


@router.delete("/{order_id}")
async def delete_order_endpoint(
        order_id: int,
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await delete_order(db, order_id)


@router.put("/cancel/{order_id}", response_model=OrderResponse)
async def cancel_order_endpoint(
        order_id: int,
        order: OrderUpdate,
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await cancel_order(db, order_id, order)
