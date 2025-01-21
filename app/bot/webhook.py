import os
from fastapi import FastAPI, Request
from aiogram import Dispatcher
from aiogram.types import Update
from .bot import bot, dp
from .handlers import router
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_DOMAIN = os.getenv("WEBHOOK_DOMAIN")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
WEBHOOK_URL = f"{WEBHOOK_DOMAIN}{WEBHOOK_PATH}"

async def init_webhook(app: FastAPI):
    """
    Вызывается при старте FastAPI
    Настраиваем webhook
    Регистрируем роуты бота
    """
    # Регистрация всех хендлеров
    dp.include_router(router)

    # Устанавливаем webhook у Telegram
    await bot.set_webhook(WEBHOOK_URL)

    # Создаём эндпоинт /webhook/bot (или из .env)
    @app.post(WEBHOOK_PATH)
    async def telegram_webhook(update: dict):
        telegram_update = Update(**update)
        await dp.feed_update(bot, telegram_update)
        return {"ok": True}
