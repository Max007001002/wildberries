from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="Получить данные по товару", callback_data="get_product_data")
    kb.adjust(1)
    return kb.as_markup()
