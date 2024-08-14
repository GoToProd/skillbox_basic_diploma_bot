from aiogram import Bot
from aiogram.types import Message, BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начало работы"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="info", description="Информация"),
        BotCommand(command="macbook", description="Вопрос о макбуке"),
        BotCommand(command="name", description="Узнать возраст по имени"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
