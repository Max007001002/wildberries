import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import Base
from .api.products import router as products_router
from .scheduler import init_scheduler
from .scheduler.jobs import schedule_articul_collection
from .bot.webhook import init_webhook  # подключаем логику вебхуков бота

app = FastAPI(
    title="Wildberries Service",
    version="1.0.0",
    description="FastAPI + Aiogram (webhook) + PostgreSQL + APScheduler"
)

# Настроим CORS при необходимости
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роуты
app.include_router(products_router, prefix="/api/v1", tags=["products"])

@app.on_event("startup")
async def on_startup():
    # Создаём таблицы в БД (если не созданы)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Запустим шедулер
    init_scheduler()

    # (Дополнительно) восстанавливаем подписки
    # Для примера: здесь можем пройтись по артикулам, которые у нас есть в БД,
    # и на каждый зарегистрировать задачу schedule_articul_collection(articul)
    # Но это уже зависит от бизнес-логики, как хранить подписки.

    # Инициализируем webhook для бота
    await init_webhook(app)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
