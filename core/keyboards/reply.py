from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# from core.handlers.basic import get_name


def get_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text="Получить случайный факт о кошках"),
    keyboard_builder.button(text="Узнать возраст по имени"),
    keyboard_builder.button(text="Посмотреть мои запросы"),
    keyboard_builder.adjust(3),
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите действие!",
    )
