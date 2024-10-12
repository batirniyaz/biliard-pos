import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.database import engine
from app.bot.main import send_telegram_message
from app.integration.light.smar_swith import light
from app.table.crud import get_all_tables


async def check_status_table():
    print("I am in check_status_table")
    try:
        async with AsyncSession(engine) as db:
            db_tables = await get_all_tables(db)
            for table in db_tables:
                table_status = light.get_status(table.id)
                if 'status' in table_status and table_status['status']:
                    print("status checked")
                    if not table.status:
                        msg = await send_telegram_message(f"Индикатор стола {table.name} горит, но заказ еще не создан")
    except Exception as e:
        print(f"Exception occurred: {e}")


async def periodic_check_status_table():
    while True:
        await check_status_table()
        await asyncio.sleep(600)


async def start_periodic_tasks():
    print("I am in start_periodic_tasks")
    task = asyncio.create_task(periodic_check_status_table())
    await task



