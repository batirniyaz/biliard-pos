import time
from collections import Counter
from datetime import datetime, timedelta
from typing import Optional

import schedule
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.menu.option.crud import get_option
from app.menu.option.model import Option
from app.menu.product.crud import get_product
from app.menu.product.model import Product
from app.table.crud import get_tables
from app.utils.time_utils import get_time, get_time_sync
from app.auth.database import get_async_session

from app.daily_report.model import DailyReport, TableReport
from app.daily_report.schema import DailyReportCreate, TableReportCreate
from app.order.model import Order


async def define_date_type(db: AsyncSession, date: str, ReportModel, table_id: Optional[int] = None):
    print("I am in define_date_type 2")
    query = select(ReportModel)

    if len(date) == 10:
        result = query.filter_by(date=date)
        if table_id:
            result = await db.execute(result.filter_by(table_id=table_id))
            report = result.scalars().all()
        else:
            result = await db.execute(result)
            report = result.scalars().first()
    else:
        result = (query.filter(ReportModel.date.startswith(date)).order_by(ReportModel.date.desc()))
        if table_id:
            result = await db.execute(result.filter_by(table_id=table_id))
            report = result.scalars().all()
        else:
            result = await db.execute(result)
            report = result.scalars().all()

    print("ending define_date_type 3")
    return report if report else []


async def get_daily_report(db: AsyncSession, date: str):
    print("I am in get_daily_report 1")
    daily_report = await define_date_type(db, date, DailyReport)
    if daily_report:
        print("made this operation")
        return daily_report
    else:
        print("made another operation")
        return await calculate_daily_report(db, date)


async def get_table_report(db: AsyncSession, date: str, table_id: Optional[int] = None):
    print("I am in get_table_report 2")
    table_report = await define_date_type(db, date, TableReport, table_id if table_id else None)
    if table_report:
        return table_report
    else:
        return await calculate_table_report(db, date, table_id if table_id else None)


async def create_daily_report(previous_date):
    previous_date = "2024-10-04"
    try:
        async for session in get_async_session():
            async with session.begin():
                daily_report = await get_daily_report(session, previous_date)

                if isinstance(daily_report, DailyReport):
                    db_daily_report = daily_report
                else:

                    db_daily_report = DailyReport(
                        date=previous_date,
                        total_income=daily_report["total_income"],
                        table_income=daily_report["table_income"],
                        product_income=daily_report["product_income"],
                        total_play_time=daily_report["total_play_time"],
                        products=daily_report["products"]
                    )
                    session.add(db_daily_report)
                    await session.flush()
                    await session.refresh(db_daily_report)
                    await session.commit()
                return db_daily_report

    except Exception as e:
        raise e


async def create_table_report(previous_date):
    try:

        async for session in get_async_session():
            async with session.begin():
                db_tables = await get_tables(session)
                for table in db_tables:
                    table_report = await calculate_table_report(session, previous_date, table.id)

                    products = []
                    total_play_time = 0
                    total_income = 0
                    for order in table_report:
                        for product in order["products"]:
                            for prod in products:
                                if prod["product_id"] == product["product_id"]:
                                    prod["quantity"] += product["quantity"]
                                else:
                                    products.append(product)
                        total_play_time += order["total_play_time"]
                        total_income += order["total_income"]

                    db_table_report = TableReport(
                        date=previous_date,
                        table_id=table.id,
                        products=products,
                        total_income=total_income,
                        total_play_time=total_play_time

                    )
                    session.add(db_table_report)
                    await session.flush()
                    await session.refresh(db_table_report)

                await session.commit()
                return db_table_report

    except Exception as e:
        raise e


async def calculate_daily_report(db, date):
    print("I am in calculate_daily_report 4")
    if len(date) == 10:
        order_query = await db.execute(select(Order).filter_by(date=date).order_by(Order.id.desc()))
    else:
        order_query = await db.execute(select(Order).filter(Order.date.startswith(date)).order_by(Order.id.desc()))

    orders = order_query.scalars().all()

    total_income = 0
    product_income = 0
    total_play_time = 0
    form_prod = []
    product_ids = []
    option_ids = []
    for order in orders:
        if order.duration is not None:
            total_play_time += order.duration
        total_income += order.total
        for product in order.products:
            product_income += product["price"]
            product_ids.append(product["product_id"])
        for option in order.options:
            product_income += option["price"]
            option_ids.append(option["option_id"])

    print(f"{product_ids=}")

    product_counts = Counter([product for product in product_ids])
    option_counts = Counter([option for option in option_ids])

    formatted_products = [{"product_id": f"{product}", "quantity": f"{count}"} for product, count in
                          product_counts.items()]
    formatted_options = [{"option_id": f"{option}", "quantity": f"{count}"} for option, count in option_counts.items()]
    form_prod.append(formatted_products + formatted_options)

    table_income = total_income - product_income
    daily_report = {
        "date": date,
        "total_income": total_income,
        "table_income": table_income,
        "products": form_prod,
        "product_income": product_income,
        "total_play_time": total_play_time,
    }
    print("ending calculation 5")
    return daily_report


async def calculate_table_report(db, date, table_id: Optional[int] = None):
    print("I am in calculate_table_report 6")
    query = select(Order)
    if table_id:
        if len(date) == 10:
            query = query.filter_by(date=date).filter_by(table_id=table_id)
        else:
            query = query.filter(Order.date.startswith(date)).filter_by(table_id=table_id)
    else:
        if len(date) == 10:
            query = query.filter_by(date=date)
        else:
            query = query.filter(Order.date.startswith(date))

    order_query = query.order_by(Order.id.desc())
    result = await db.execute(order_query)
    orders = result.scalars().all()

    table_report = []
    form_prod = []
    for order in orders:
        products = []
        product_price = 0
        product_count = Counter([product['product_id'] for product in order.products])
        option_count = Counter([option['option_id'] for option in order.options])

        formatted_products = [{"product_id": f"{product}", "quantity": f"{count}"} for product, count in
                              product_count.items()]
        formatted_options = [{"option_id": f"{option}", "quantity": f"{count}"} for option, count in
                             option_count.items()]
        form_prod = formatted_products + formatted_options

        for product in order.products:
            db_product = await db.execute(select(Product).filter_by(id=product["product_id"]))
            db_product = db_product.scalars().first()
            if not db_product:
                continue
            products.append({
                "product_id": db_product.id,
                "product_name": db_product.name,
                "price": db_product.price,
                "quantity": product_count[product["product_id"]]
            })
            product_price += db_product.price

        for option in order.options:
            db_option = await db.execute(select(Option).filter_by(id=option["option_id"]))
            db_option = db_option.scalars().first()
            if not db_option:
                continue
            products.append({
                "option_id": db_option.id,
                "option_name": db_option.name,
                "price": db_option.price,
                "quantity": option_count[option["option_id"]]
            })
            product_price += db_option.price

        table_report.append({
            "order_id": order.id,
            "table_name": order.table_name,
            "table_price": order.table_price,
            "start_time": order.start_time,
            "product_income": product_price,
            "products": form_prod,
            "end_time": order.end_time,
            "total_play_time": order.duration,
            "date": order.date,
            "total_income": order.total,
        })

    return table_report


# def schedule_daily_report():
#     _, current_date = get_time()
#     schedule_time = datetime.now(current_date).replace(hour=23, minute=30, second=0, microsecond=0)
#     schedule.every().day.at(schedule_time.strftime("%H:%M")).do(lambda: asyncio.create_task(store_daily_report()))
