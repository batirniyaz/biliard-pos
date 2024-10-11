from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth.auth_backend import current_active_user
from app.auth.database import get_async_session, User
from app.daily_report.crud import get_daily_report, get_table_report, close_session
from app.utils.check_util import history_check, check_helper

router = APIRouter()


@router.get("/daily")
@cache(expire=60)
async def get_daily_report_endpoint(
        date: str = Query(
            ...,
            description="The date of the daily report",
            alias="daily_report_date"),
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)

):
    if not current_user.is_superuser:
        raise Exception("Only superuser can get daily report")
    return await get_daily_report(db, date)


@router.get("/table")
@cache(expire=60)
async def get_table_report_endpoint(
        date: str = Query(
            ...,
            description="The date of the daily report",
            alias="daily_report_date"),
        table_id: Optional[int] = Query(None, description="The id of the table", alias="table_id"),
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)

):
    if not current_user.is_superuser:
        raise Exception("Only superuser can get table report")
    return await get_table_report(db, date, table_id if table_id else None)


@router.get("/close_session")
async def close_session_endpoint(
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await close_session(db)


@router.get("/session_history")
@cache(expire=60)
async def session_history_endpoint(
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await history_check(db)


@router.get("/print_check")
async def print_check_endpoint(
        order_id: int = Query(..., description="The id of the order", alias="order_id"),
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await check_helper(db, order_id)
