import os
import asyncio
import logging
from dotenv.main import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from core.handlers.basic import (
    get_start,
    get_help,
    get_info,
    get_echo,
    get_macbook_info,
    get_cat,
    get_name,
    check_name,
    get_answer,
    get_requests,
)
from core.handlers.callback import select_makbook
from core.utils.commands import set_commands
from core.utils.statesform import StepsForm
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.jobstores.redis import RedisJobStore


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(ADMIN_ID, text="Бот запущен!")


async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN_ID, text="Бот остановлен")


async def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - [%(name)s] - [%(filename)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d - %(message)s",
    )

    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

    storage = RedisStorage.from_url("redis://localhost:6379/0")

    dp = Dispatcher(storage=storage)

    jobstores = {
        "default": RedisJobStore(
            jobs_key="dispatched_trips_jobs",
            run_times_key="dispatched_trips_running",
            host="localhost",
            db=2,
            port=6379,
        )
    }

    scheduler = ContextSchedulerDecorator(
        AsyncIOScheduler(timezone="Europe/Moscow", jobstores=jobstores)
    )
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.start()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_start, Command(commands=["start", "run"]))
    dp.message.register(get_help, Command(commands=["help"]))
    dp.message.register(get_info, Command(commands=["info"]))
    dp.message.register(get_macbook_info, Command(commands=["macbook"]))
    dp.message.register(get_cat, F.text == "Получить случайный факт о кошках")
    dp.message.register(get_name, Command(commands=["name"]))
    dp.message.register(get_name, F.text == "Узнать возраст по имени")
    dp.message.register(get_requests, F.text == "Посмотреть мои запросы")
    dp.message.register(check_name, StepsForm.GET_NAME)
    dp.message.register(get_answer, StepsForm.GET_ANSWER)
    dp.message.register(get_echo)
    dp.callback_query.register(select_makbook)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
