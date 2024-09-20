from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.table.model import Table
from app.table.schema import TableCreate, TableUpdate


async def create_table(db: AsyncSession, table: TableCreate):
    try:
        db_table = Table(**table.model_dump())
        db.add(db_table)
        await db.commit()
        await db.refresh(db_table)
        return db_table
    except Exception as e:
        await db.rollback()
        raise e


async def get_table(db: AsyncSession, table_id: int):
    res = await db.execute(select(Table).filter_by(id=table_id))
    db_table = res.scalars().first()

    if not db_table:
        raise Exception("Table not found")

    return db_table


async def get_all_tables(db: AsyncSession):
    res = await db.execute(select(Table))
    tables = res.scalars().all()
    return tables


async def update_table(db: AsyncSession, table_id: int, table: TableUpdate):
    res = await db.execute(select(Table).filter_by(id=table_id))
    db_table = res.scalars().first()

    if not db_table:
        raise Exception("Table not found")

    for key, value in table.model_dump(exclude_unset=True).items():
        setattr(db_table, key, value)

    db.add(db_table)
    await db.commit()
    await db.refresh(db_table)

    return db_table


async def delete_table(db: AsyncSession, table_id: int):
    res = await db.execute(select(Table).filter_by(id=table_id))
    db_table = res.scalars().first()

    if not db_table:
        raise Exception("Table not found")

    await db.delete(db_table)
    await db.commit()
    return db_table
