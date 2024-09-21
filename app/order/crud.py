from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.attributes import flag_modified

from app.menu.option.crud import get_option
from app.menu.product.model import Product
from app.order.model import Order
from app.order.schema import OrderCreate, OrderUpdate
from app.table.crud import get_table, update_table
from app.utils.time_utils import get_time

from app.menu.product.crud import get_product


async def create_order(db: AsyncSession, order: OrderCreate):
    try:
        table = await get_table(db, order.table_id)
        if not table.status:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Table is already occupied")

        table.status = False

        start_time, date = await get_time()
        db_order = Order(
            **order.model_dump(),
            start_time=start_time,
            date=date,
            table_name=table.name,
            table_status=table.status
        )
        db.add(db_order)
        await db.commit()
        await db.refresh(db_order)
        await db.refresh(table)

        return db_order
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_orders(db: AsyncSession):
    result = await db.execute(select(Order).where(Order.status == True))
    orders = result.scalars().all()

    return orders if orders else []


async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).filter_by(id=order_id))
    order = result.scalars().first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    return order


async def update_order(db: AsyncSession, order_id: int, order: OrderUpdate):
    try:
        db_order = await get_order(db, order_id)
        table = await get_table(db, db_order.table_id)

        if table.status:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Table is not occupied")

        total_price = db_order.total

        for product in order.products:
            db_product = await get_product(db, product)
            db_order.products.append({
                "product_id": db_product.id,
                "product_name": db_product.name,
                "price": db_product.price
            })
            total_price += db_product.price

        for option in order.options:
            db_option = await get_option(db, option)
            db_order.options.append({
                "option_id": db_option.id,
                "option_name": db_option.name,
                "price": db_option.price
            })
            total_price += db_option.price

        if not order.status:

            db_order.end_time, _ = await get_time()
            start_time_obj = datetime.strptime(db_order.start_time, "%H:%M:%S")
            end_time_obj = datetime.strptime(db_order.end_time, "%H:%M:%S")
            db_order.duration = int((end_time_obj - start_time_obj).total_seconds() / 60)  # in minutes
            price_per_minutes = int(table.price / 60)  # price per minute
            total_duration = db_order.duration * price_per_minutes
            total_price += total_duration

            table.status = True

        db_order.total = total_price

        flag_modified(db_order, "options")
        flag_modified(db_order, "products")
        flag_modified(db_order, "total")
        flag_modified(table, "status")

        await db.commit()
        await db.refresh(db_order)
        await db.refresh(table)

        return db_order
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
