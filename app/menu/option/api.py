from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth.auth_backend import current_active_user
from app.auth.database import get_async_session, User

from app.menu.option.crud import create_option, get_options, get_option, update_option, delete_option
from app.menu.option.schema import OptionCreate, OptionUpdate, OptionResponse


router = APIRouter()


@router.post("/", response_model=OptionResponse)
async def create_option_endpoint(
        option: OptionCreate,
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    return await create_option(db, option)


@router.get("/", )
async def get_options_endpoint(
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await get_options(db)


@router.get("/{option_id}")
async def get_option_endpoint(
        option_id: int,
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await get_option(db, option_id)


@router.put("/{option_id}", response_model=OptionResponse)
async def update_option_endpoint(
        option_id: int,
        option: OptionUpdate,
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await update_option(db, option_id, option)


@router.delete("/{option_id}")
async def delete_option_endpoint(
        option_id: int,
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(current_active_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await delete_option(db, option_id)
