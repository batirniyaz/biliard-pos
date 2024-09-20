from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.menu.option.model import Option
from app.menu.option.schema import OptionCreate, OptionUpdate

from app.menu.product.crud import get_product


async def create_option(db: AsyncSession, option: OptionCreate):
    try:
        db_option = Option(**option.model_dump())
        db.add(db_option)
        await db.commit()
        await db.refresh(db_option)

        return db_option
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_options(db: AsyncSession):
    result = await db.execute(select(Option))
    options = result.scalars().all()

    return options if options else []


async def get_option(db: AsyncSession, option_id: int):
    result = await db.execute(select(Option).filter_by(id=option_id))
    option = result.scalars().first()

    if not option:
        raise HTTPException(status_code=404, detail="Option not found")

    return option


async def update_option(db: AsyncSession, option_id: int, option: OptionUpdate):
    try:
        db_option = await get_option(db, option_id)
        db_product = await get_product(db, option.product_id)

        for key, value in option.model_dump().items():
            setattr(db_option, key, value)

        await db.commit()
        await db.refresh(db_option)

        return db_option
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_option(db: AsyncSession, option_id: int):
    try:
        db_option = await get_option(db, option_id)

        await db.delete(db_option)
        await db.commit()

        return {"message": "Option deleted successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
