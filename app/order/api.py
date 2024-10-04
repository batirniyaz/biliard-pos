from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.database import get_async_session

from app.order.schema import OrderCreate, OrderResponse, OrderUpdate
from app.order.crud import create_order, update_order, get_order, get_orders, delete_order, get_all_orders, cancel_order

router = APIRouter()


@router.post("/", response_model=OrderResponse)
async def create_order_endpoint(
        order: OrderCreate,
        db: AsyncSession = Depends(get_async_session)
):
    return await create_order(db, order)


@router.get("/all", response_model=List[OrderResponse])
async def get_all_orders_endpoint(
        db: AsyncSession = Depends(get_async_session)
):
    return await get_all_orders(db)


@router.get("/", response_model=List[OrderResponse])
async def get_orders_endpoint(
        db: AsyncSession = Depends(get_async_session)
):
    return await get_orders(db)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_endpoint(
        order_id: int,
        db: AsyncSession = Depends(get_async_session)
):
    return await get_order(db, order_id)


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order_endpoint(
        order_id: int,
        order: OrderUpdate,
        db: AsyncSession = Depends(get_async_session)
):
    return await update_order(db, order_id, order)


@router.delete("/{order_id}")
async def delete_order_endpoint(
        order_id: int,
        db: AsyncSession = Depends(get_async_session)
):
    return await delete_order(db, order_id)


@router.put("/cancel/{order_id}", response_model=OrderResponse)
async def cancel_order_endpoint(
        order_id: int,
        order: OrderUpdate,
        db: AsyncSession = Depends(get_async_session)
):
    return await cancel_order(db, order_id, order)