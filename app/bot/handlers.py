from aiogram import Router, types, F
from aiogram.filters import Command
from .keyboards import main_menu
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_session
from ..crud import get_product_by_articul

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать! Нажмите на кнопку, чтобы получить данные по товару.",
        reply_markup=main_menu()
    )

@router.callback_query(F.data == "get_product_data")
async def on_get_product_data(call: types.CallbackQuery):
    """
    Обработчик нажатия кнопки "Получить данные по товару"
    """
    await call.message.answer("Пожалуйста, введите артикул товара:")
    await call.answer()  # уберём "часики" на кнопке

@router.message()
async def receive_articul(message: types.Message):
    """
    Здесь примем любое сообщение пользователя как артикул,
    и попробуем поискать его в БД
    """
    articul = message.text.strip()
    # запросим данные из БД
    async for session in get_session():
        product = await get_product_by_articul(session, articul)

    if product:
        response_text = (
            f"Название: {product.name}\n"
            f"Артикул: {product.articul}\n"
            f"Цена: {product.price}\n"
            f"Рейтинг: {product.rating}\n"
            f"Суммарное количество: {product.total_quantity}"
        )
    else:
        response_text = "Товар не найден в БД. Попробуйте сначала выполнить /api/v1/products."

    await message.answer(response_text)
