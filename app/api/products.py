import httpx
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_session
from ..schemas import ProductRequest, ProductCreate, ProductOut
from ..crud import create_or_update_product
from ..scheduler.jobs import schedule_articul_collection
import os

router = APIRouter()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")

def authorize(token: str = Header(None)):
    # Реализуем простую Bearer-авторизацию
    if token != f"Bearer {BEARER_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

# Асинхронная функция для получения данных о товаре с Wildberries
async def fetch_product_data(articul: str):
    url = "https://card.wb.ru/cards/v1/detail"
    params = {
        "appType": 1,
        "curr": "rub",
        "dest": -1257786,
        "spp": 30,
        "nm": articul
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        return response.json()

@router.post("/products", response_model=ProductOut)
async def create_product(
        product_req: ProductRequest,
        db: AsyncSession = Depends(get_session),
        auth: None = Depends(authorize)  # если нужна авторизация
):
    """
    Эндпоинт POST /api/v1/products.
    Принимает {"artikul": ...}, делает запрос в WB API, сохраняет в БД.
    """
    data = await fetch_product_data(product_req.articul)
    try:
        product_data = data["data"]["products"][0]
        name = product_data["name"]
        price = product_data["salePriceU"] / 100  # Цена в копейках
        rating = product_data.get("rating", 0)
        total_quantity = sum(size["qty"] for size in product_data["sizes"] if "qty" in size)
    except (KeyError, IndexError):
        raise HTTPException(status_code=400, detail="Неверная структура ответа от WB")

    product_create = ProductCreate(
        articul=product_req.articul,
        name=name,
        price=price,
        rating=rating,
        total_quantity=total_quantity
    )

    product = await create_or_update_product(db, product_create)

    return product

@router.get("/subscribe/{articul}", response_model=ProductOut)
async def subscribe_articul(
        articul: str,
        db: AsyncSession = Depends(get_session),
        auth: None = Depends(authorize)
):
    """
    GET /api/v1/subscribe/{articul}.
    Запускает периодический сбор данных в БД раз в 30 минут.
    """
    # Сразу сделаем первоначальный сбор (одноразовый вызов логики):
    data = await fetch_product_data(articul)
    try:
        product_data = data["data"]["products"][0]
        name = product_data["name"]
        price = product_data["salePriceU"] / 100
        rating = product_data.get("rating", 0)
        total_quantity = sum(size["qty"] for size in product_data["sizes"] if "qty" in size)
    except (KeyError, IndexError):
        raise HTTPException(status_code=400, detail="Неверная структура ответа от WB")

    product_create = ProductCreate(
        articul=articul,
        name=name,
        price=price,
        rating=rating,
        total_quantity=total_quantity
    )

    product = await create_or_update_product(db, product_create)

    # Запускаем задачу в APScheduler на сбор данных каждые 30 минут.
    await schedule_articul_collection(articul)

    return product
