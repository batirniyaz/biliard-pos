from collections import Counter
from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.attributes import flag_modified

from app.bot.main import send_telegram_message
from app.menu.option.crud import get_option
from app.order.model import Order
from app.order.schema import OrderCreate, OrderUpdate
from app.table.crud import get_table
from app.utils.time_utils import get_time
from app.utils.check_util import print_check

from app.menu.product.crud import get_product

from app.integration.light.smar_swith import turn_off, turn_on


async def create_order(db: AsyncSession, order: OrderCreate):
    try:
        light_response = turn_on(order.table_id)

        table = await get_table(db, order.table_id)
        if not table.status:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Table is already occupied")

        table.status = False

        uzb_time = await get_time()
        date = uzb_time.strftime("%Y-%m-%d")
        start_time = uzb_time.strftime("%H:%M:%S")

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
            f"Order created on {db_order.table_name} with order id: {db_order.id} \nOn time: {db_order.start_time} \n\n"
            f'{"The light was on" if not light_response["response"] else "The light turned on successfully"}',
        )

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

            light_response = turn_off(db_order.table_id)

            uzb_time = await get_time()
            db_order.end_time = uzb_time.strftime("%H:%M:%S")
            start_datetime_obj = datetime.strptime(f"{db_order.date} {db_order.start_time}", "%Y-%m-%d %H:%M:%S")
            end_datetime_obj = uzb_time
            db_order.duration = int((end_datetime_obj - start_datetime_obj).total_seconds() / 60)  # in minutes
            price_per_minutes = int(table.price / 60)  # price per minute
            total_duration = db_order.duration * price_per_minutes
            round_table_price = ((total_duration + 499) // 500) * 500
            total_price += round_table_price

            db_order.table_income = round_table_price

            table.status = True
            db_order.table_status = table.status

            product_counts = Counter([product['product_name'] for product in db_order.products])
            option_counts = Counter([option['option_name'] for option in db_order.options])

            formatted_products = [f"{product} x{count}" for product, count in product_counts.items()]
            formatted_options = [f"{option} x{count}" for option, count in option_counts.items()]

            changed_status = False
            end_date = uzb_time.strftime("%Y-%m-%d")
            if end_date != db_order.date:
                changed_status = True

            db_order.products_income = db_order.total
            await send_telegram_message(
                f"Order ended on {db_order.table_name} with order id: {db_order.id}"
                f"\n\nTotal price: {total_price} UZS"
                f"\nStart time: {db_order.start_time if not changed_status else (db_order.date, db_order.start_time)} "
                f"\t End time: {db_order.end_time}"
                f"\nDuration: {db_order.duration} minutes"
                f"\nTable price: {round_table_price} UZS"
                f"\nProducts price: {db_order.total} UZS"
                f"\n\nProducts: {', '.join(formatted_products + formatted_options)} \n\n"
                f'{"The light was off" if not light_response["response"] else "The light turned off successfully"}',
            )

        check = print_check(db_order)

        db_order.status = order.status

        db_order.total = total_price

        flag_modified(db_order, "options")
        flag_modified(db_order, "products")
        flag_modified(db_order, "total")
        flag_modified(table, "status")
        flag_modified(db_order, "products_income")
        flag_modified(db_order, "table_income")

        await db.commit()
        await db.refresh(db_order)
        await db.refresh(table)

        return db_order, check
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


async def cancel_order(db: AsyncSession, order_id: int, order: OrderUpdate):
    try:
        db_order = await get_order(db, order_id)
        db_table = await get_table(db, db_order.table_id)

        if db_table.status:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Table is not occupied")

        if not db_order.status:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order already ended")

        for product_id in order.products:
            for product in db_order.products:
                if product["product_id"] == product_id:
                    db_product = await get_product(db, product_id)
                    db_order.products.remove(product)
                    db_order.total -= db_product.price
                    break

        for option_id in order.options:
            for option in db_order.options:
                if option["option_id"] == option_id:
                    db_option = await get_option(db, option_id)
                    db_order.options.remove(option)
                    db_order.total -= db_option.price
                    break

        flag_modified(db_order, "products")
        flag_modified(db_order, "options")
        flag_modified(db_order, "total")

        await db.commit()
        await db.refresh(db_order)

        return db_order
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
