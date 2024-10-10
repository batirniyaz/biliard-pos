from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.integration.check.main import prn_txt
from app.order.model import Order


def print_check(db_order):
    try:
        if not db_order.status:

            json_order = {
                "id": db_order.id,
                "table_id": db_order.table_id,
                "table_name": db_order.table_name,
                "table_price": db_order.table_price,
                "table_status": db_order.table_status,
                "start_time": db_order.start_time,
                "products": db_order.products,
                "options": db_order.options,
                "end_time": db_order.end_time,
                "duration": db_order.duration,
                "table_income": db_order.table_income,
                "products_income": db_order.products_income,
                "total": db_order.total,
                "date": db_order.date,
                "status": db_order.status,
            }

            check = prn_txt(json_order)
            return check
    except Exception as e:
        return str(e)


async def check_helper(db: AsyncSession, order_id: int):
    from app.order.crud import get_order

    db_order = await get_order(db, order_id)
    return print_check(db_order)


async def history_check(db: AsyncSession):
    res = await db.execute(select(Order).filter_by(report_status=True).order_by(Order.id.desc()))
    db_orders = res.scalars().all()
    return db_orders if db_orders else []
