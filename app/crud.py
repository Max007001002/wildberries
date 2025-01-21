from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Product
from .schemas import ProductCreate

# Создание или обновление товара
async def create_or_update_product(db: AsyncSession, product_data: ProductCreate):
    result = await db.execute(select(Product).where(Product.articul == product_data.articul))
    existing_product = result.scalars().first()

    if existing_product:
        existing_product.name = product_data.name
        existing_product.price = product_data.price
        existing_product.rating = product_data.rating
        existing_product.total_quantity = product_data.total_quantity
        await db.commit()
        await db.refresh(existing_product)
        return existing_product
    else:
        new_product = Product(**product_data.dict())
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return new_product

# Получение товара по артикулу
async def get_product_by_articul(db: AsyncSession, articul: str):
    result = await db.execute(select(Product).where(Product.articul == articul))
    return result.scalars().first()
