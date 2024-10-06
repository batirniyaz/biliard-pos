from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.database import get_async_session
from app.daily_report.crud import get_daily_report, get_table_report, close_session

router = APIRouter()


@router.get("/daily")
async def get_daily_report_endpoint(
        date: str = Query(
            ...,
            description="The date of the daily report",
            alias="daily_report_date"),
        db: AsyncSession = Depends(get_async_session)
):
    return await get_daily_report(db, date)


@router.get("/table")
async def get_table_report_endpoint(
        date: str = Query(
            ...,
            description="The date of the daily report",
            alias="daily_report_date"),
        table_id: Optional[int] = Query(None, description="The id of the table", alias="table_id"),
        db: AsyncSession = Depends(get_async_session)

):
    return await get_table_report(db, date, table_id if table_id else None)


@router.get("/close_session")
async def close_session_endpoint(
        db: AsyncSession = Depends(get_async_session)
):
    return await close_session(db)
