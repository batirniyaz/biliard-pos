from fastapi import APIRouter
from app.table.api import router as table_router

router = APIRouter()

router.include_router(table_router, prefix="/table", tags=["Table"])

