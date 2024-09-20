from typing import Union, Optional

from fastapi import HTTPException, UploadFile

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.utils.file_utils import save_upload_file

from app.menu.product.model import Product
from app.menu.product.schema import ProductCreate, ProductUpdate


async def create_product(db: AsyncSession, product: ProductCreate, image: UploadFile):
    try:

        main_image_url, file_path = save_upload_file(image)
        image_url = f"{main_image_url}{file_path}"

        db_product = Product(**product.model_dump(), image=image_url, options=[])

        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)

        return db_product
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    products = result.scalars().all()

    return products


async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).filter_by(id=product_id))
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


async def update_product(
        db: AsyncSession, product_id: int, product: ProductUpdate, image: Union[Optional[UploadFile], str]
):
    res_db_product = await db.execute(select(Product).filter_by(id=product_id))
    db_product = res_db_product.scalars().first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.model_dump().items():
        if value is not None:
            setattr(db_product, key, value)

    if image:
        main_image_url, file_path = save_upload_file(image)
        image_url = f"{main_image_url}{file_path}"
        db_product.image = image_url

    await db.commit()
    await db.refresh(db_product)

    return db_product


async def delete_product(db: AsyncSession, product_id: int):
    db_product = await get_product(db, product_id)

    if db_product.options:
        raise HTTPException(status_code=400, detail="Product has options. Please delete them first.")

    await db.delete(db_product)
    await db.commit()

    return {"message": "Product deleted successfully."}
