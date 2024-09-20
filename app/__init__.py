from fastapi import APIRouter
from app.table.api import router as table_router
from app.menu.product.api import router as product_router
from app.menu.option.api import router as option_router

router = APIRouter()

router.include_router(table_router, prefix="/table", tags=["Table"])
router.include_router(product_router, prefix="/product", tags=["Product"])
router.include_router(option_router, prefix="/option", tags=["Option"])

