from collections import Counter
from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.attributes import flag_modified

from app.bot.main import send_telegram_message
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
            table_status=table.status,
            table_price=table.price,
        )
        db.add(db_order)
        await db.commit()
        await db.refresh(db_order)
        await db.refresh(table)

        await send_telegram_message(
            f"Order created on {db_order.table_name} with order id: {db_order.id} \nOn time: {db_order.start_time}")

        return db_order
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_all_orders(db: AsyncSession):
    result = await db.execute(select(Order))
    orders = result.scalars().all()

    return orders if orders else []


async def get_orders(db: AsyncSession):
    result = await db.execute(select(Order).filter_by(status=True))
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
        # if not order.status:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order is already ended")

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
            round_table_price = ((total_duration + 499) // 500) * 500
            total_price += round_table_price

            table.status = True
            db_order.table_status = table.status

            product_counts = Counter([product['product_name'] for product in db_order.products])
            option_counts = Counter([option['option_name'] for option in db_order.options])

            formatted_products = [f"{product} x{count}" for product, count in product_counts.items()]
            formatted_options = [f"{option} x{count}" for option, count in option_counts.items()]

            await send_telegram_message(
                f"Order ended on {db_order.table_name} with order id: {db_order.id}"
                f"\n\nTotal price: {total_price} UZS"
                f"\nStart time: {db_order.start_time} \t End time: {db_order.end_time}"
                f"\nDuration: {db_order.duration} minutes"
                f"\nTable price: {round_table_price} UZS"
                f"\nProducts price: {db_order.total} UZS"
                f"\n\nProducts: {', '.join(formatted_products + formatted_options)}"
            )

        db_order.status = order.status

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


async def delete_order(db: AsyncSession, order_id: int):
    try:
        db_order = await get_order(db, order_id)

        await db.delete(db_order)
        await db.commit()

        return {"message": "Order deleted successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
