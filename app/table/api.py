from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.table.crud import get_all_tables, get_table, create_table, update_table, delete_table
from app.table.schema import TableResponse, TableCreate, TableUpdate
from app.auth.database import get_async_session

router = APIRouter()


@router.post("/", response_model=TableResponse)
async def create_table_endpoint(
        table: TableCreate,
        db=Depends(get_async_session)
):
    try:
        return await create_table(db, table)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[TableResponse])
async def get_all_tables_endpoint(
        db=Depends(get_async_session)
):
    try:
        return await get_all_tables(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{table_id}", response_model=TableResponse)
async def get_table_endpoint(
        table_id: int,
        db=Depends(get_async_session)
):
    try:
        return await get_table(db, table_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{table_id}", response_model=TableResponse)
async def update_table_endpoint(
        table_id: int,
        table: TableUpdate,
        db=Depends(get_async_session)
):
    try:
        return await update_table(db, table_id, table)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{table_id}")
async def delete_table_endpoint(
        table_id: int,
        db=Depends(get_async_session)
):
    try:
        return await delete_table(db, table_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
