from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache

from app.auth.auth_backend import current_active_user
from app.table.crud import get_all_tables, get_table, create_table, update_table, delete_table, get_tables
from app.table.schema import TableResponse, TableCreate, TableUpdate
from app.auth.database import get_async_session, User

router = APIRouter()


@router.post("/", response_model=TableResponse)
async def create_table_endpoint(
        table: TableCreate,
        db=Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    try:
        return await create_table(db, table)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/all", response_model=List[TableResponse])
@cache(expire=60)
async def get_all_tables_endpoint(
        db=Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    try:
        return await get_all_tables(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[TableResponse])
@cache(expire=60)
async def get_tables_endpoint(
        db=Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    try:
        return await get_tables(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{table_id}", response_model=TableResponse)
@cache(expire=60)
async def get_table_endpoint(
        table_id: int,
        db=Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    try:
        return await get_table(db, table_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{table_id}", response_model=TableResponse)
async def update_table_endpoint(
        table_id: int,
        table: TableUpdate,
        db=Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    try:
        return await update_table(db, table_id, table)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{table_id}")
async def delete_table_endpoint(
        table_id: int,
        db=Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    try:
        return await delete_table(db, table_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
