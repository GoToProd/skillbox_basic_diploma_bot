import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.callbackdata import MacInfo
from dotenv import load_dotenv

load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")


def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(
        text="Macbook Air 13",
        callback_data=MacInfo(model="air", size="13", chip="m1", year="2020"),
    )
    keyboard_builder.button(
        text="Macbook Pro 14",
        callback_data=MacInfo(model="pro", size="14", chip="m2", year="2022"),
    )
    keyboard_builder.button(
        text="Никакой",
        callback_data=MacInfo(model="none", size="0", chip="none", year="0"),
    )
    keyboard_builder.button(text="Сайт компании Apple", url="https://www.apple.com/")
    keyboard_builder.button(
        text="Профиль разработчика", url=f"tg://user?id={ADMIN_ID}"
    ),

    keyboard_builder.adjust(3)

    return keyboard_builder.as_markup()
