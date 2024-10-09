from collections import Counter
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.table.crud import get_tables
from app.utils.time_utils import get_time_sync

from app.daily_report.model import DailyReport, TableReport
from app.order.model import Order


async def define_date_type(db: AsyncSession, date: str, ReportModel, table_id: Optional[int] = None):
    print("I am in define_date_type 2")
    query = select(ReportModel)

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
    return daily_report if daily_report else []


async def get_table_report(db: AsyncSession, date: str, table_id: Optional[int] = None):
    print("I am in get_table_report 2")
    table_report = await define_date_type(db, date, TableReport, table_id if table_id else None)
    return table_report if table_report else []


def serialize_order(order):
    return {
        "id": order.id,
        "date": order.date,
        "table_income": order.table_income,
        "products_income": order.products_income,
        "total": order.total,
        "duration": order.duration,
        "products": order.products,
        "options": order.options,
        "table_id": order.table_id,
        "table_name": order.table_name,
        "table_price": order.table_price,
        "table_status": order.table_status,
        "start_time": order.start_time,
        "end_time": order.end_time,
        "status": order.status,
    }


async def calculate_daily_report(db):
    print("I am in calculate_daily_report 4")
    result = await db.execute(select(Order).filter_by(report_status=True).order_by(Order.id.desc()))
    orders = result.scalars().all()

    res_daily = await calculation(orders)

    serialized_orders = [serialize_order(order) for order in orders]

    db_daily_report = DailyReport(
        date=res_daily["date"],
        total_income=res_daily["total_income"],
        table_income=res_daily["table_income"],
        product_income=res_daily["product_income"],
        total_play_time=res_daily["total_play_time"],
        products=res_daily["products"],
        orders=serialized_orders,
    )
    db.add(db_daily_report)
    await db.commit()
    await db.refresh(db_daily_report)

    print("ending calculation 5")
    return db_daily_report


async def calculate_table_report(db):
    print("I am in calculate_table_report 6")
    db_tables = await get_tables(db)

    db_tables_report = []

    for table in db_tables:
        query = select(Order).filter_by(table_id=table.id).filter_by(report_status=True).order_by(Order.id.desc())

        result = await db.execute(query)
        orders = result.scalars().all()

        res_table = await calculation(orders)

        for order in orders:
            order.report_status = False
            db.add(order)
            await db.commit()
            await db.refresh(order)

        serialized_orders = [serialize_order(order) for order in orders]

        db_table_report = TableReport(
            date=res_table["date"],
            table_id=table.id,
            products=res_table["products"],
            table_income=res_table["table_income"],
            products_income=res_table["product_income"],
            total_income=res_table["total_income"],
            total_play_time=res_table["total_play_time"],
            orders=serialized_orders
        )
        db_tables_report.append(db_table_report)

        db.add(db_table_report)
        await db.commit()
        await db.refresh(db_table_report)

    return db_tables_report


async def calculation(orders):
    uzb_time = get_time_sync()
    print(f"{uzb_time=}")
    date = uzb_time.strftime("%Y-%m-%d")
    time_uzb = uzb_time.strftime("%H:%M:%S")
    datetime_uzb = f"{date} {time_uzb}"

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

    db_report = {
        "date": datetime_uzb,
        "total_income": total_income,
        "table_income": table_income,
        "product_income": product_income,
        "total_play_time": total_play_time,
        "products": formatted_products + formatted_options,
        "orders": orders
    }
    return db_report


async def close_session(db: AsyncSession):

    daily_report = await calculate_daily_report(db)

    table_report = await calculate_table_report(db)

    return {"daily_report": daily_report, "table_report": table_report}





