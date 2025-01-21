import os
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_session
from ..crud import create_or_update_product
from ..schemas import ProductCreate
from fastapi import HTTPException

scheduler = AsyncIOScheduler()

async def collect_data_for_articul(articul: str):
    """
    Собирает данные по указанному артикулу и обновляет БД.
    Вызывается шедулером каждые 30 минут (и вручную при subscribe).
    """
    from ..database import async_session  # чтобы не было циклического импорта

    url = "https://card.wb.ru/cards/v1/detail"
    params = {
        "appType": 1,
        "curr": "rub",
        "dest": -1257786,
        "spp": 30,
        "nm": articul
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return

    data = response.json()
    try:
        product_data = data["data"]["products"][0]
        name = product_data["name"]
        price = product_data["salePriceU"] / 100
        rating = product_data.get("rating", 0)
        total_quantity = sum(size["qty"] for size in product_data["sizes"] if "qty" in size)
    except (KeyError, IndexError):
        return

    product_create = ProductCreate(
        articul=articul,
        name=name,
        price=price,
        rating=rating,
        total_quantity=total_quantity
    )

    # Создадим/обновим в БД
    async with async_session() as session:
        await create_or_update_product(session, product_create)


async def schedule_articul_collection(articul: str):
    """
    Регистрируем (или перерегистрируем) задачу на каждые 30 минут.
    """
    # Сначала уберём старую задачу, если была (чтобы не плодить дублей)
    job_id = f"collect_{articul}"
    scheduler.remove_job(job_id, jobstore=None, job_kwargs=None, silence_errors=True)

    # Теперь добавим новую
    scheduler.add_job(
        collect_data_for_articul,
        "interval",
        minutes=30,
        args=[articul],
        id=job_id,
        replace_existing=True
    )
