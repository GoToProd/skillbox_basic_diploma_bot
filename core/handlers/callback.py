from aiogram import Bot
from aiogram.types import CallbackQuery, Message


async def select_makbook(call: CallbackQuery, bot: Bot):
    if call.data.split(":")[1] == "none":
        answer = f"Очень жаль. Многое потеряли!"
    else:
        model = call.data.split(":")[1]
        size = call.data.split(":")[2]
        chip = call.data.split(":")[3]
        year = call.data.split(":")[4]
        answer = f"КРАСАВА!!!!!! \nApple {model} {size} {chip} {year} это очень круто!"
    await call.message.answer(answer)
    await call.answer()
