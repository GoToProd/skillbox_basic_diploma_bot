import ssl
import certifi
from core.config import ADMIN_ID
from aiogram import Bot
from aiogram.types import Message
import aiohttp
from googletrans import Translator
from transliterate import translit
from core.keyboards.reply import get_reply_keyboard
from core.keyboards.inline import get_inline_keyboard
import asyncio
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.context import FSMContext
from core.utils.statesform import StepsForm
from core.utils.check_language import is_russian_word

from core.database.models import User
from core.database.db_commands import (
    add_user,
    add_request,
    get_user_by_username,
    get_user_requests,
)


async def get_start(message: Message, bot: Bot):
    user = User.get_or_none(User.user_name == message.from_user.username)
    if not user:
        user = await add_user(message.from_user.username, message.from_user.first_name)
        await bot.send_message(
            ADMIN_ID,
            f"Новый пользователь - {message.from_user.first_name}, tg://user?id={message.from_user.id}",
        )
        await add_request(user, "/start")
        async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
            await asyncio.sleep(1)
            await message.answer(
                f"Здравствуйте, уважаемый <b>{message.from_user.first_name.title()}</b>. \nРад вас видеть в моем учебном боте!",
                reply_markup=get_reply_keyboard(),
            )
    await add_request(user, "/start")
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        await asyncio.sleep(1)
        await message.answer(
            f"Вы уже нажали start! Уважаемый <b>{message.from_user.first_name.title()}</b>, хватит!. \n Но, я снова рад вас видеть в моем учебном боте!",
            reply_markup=get_reply_keyboard(),
        )


async def get_help(message: Message, bot: Bot):
    user = await get_user_by_username(message.from_user.username)
    if user:
        await add_request(user, "/help")

    async with ChatActionSender.upload_video(bot=bot, chat_id=message.from_user.id):
        await asyncio.sleep(1)
        await message.answer(
            f"Помогу чем смогу, но на бота надейся, а сам не плошай!\n"
            f"В боте есть такие команды как: \n/start\t /help \t/info \t/macbook \t/name\n"
            f"Данные команды выполняют какой-либо функционал, затестируйте их! :)"
        )


async def get_info(message: Message, bot: Bot):
    user = await get_user_by_username(message.from_user.username)
    if user:
        await add_request(user, "/info")

    async with ChatActionSender.upload_document(bot=bot, chat_id=message.from_user.id):
        await asyncio.sleep(1)
        await message.answer(
            f"Д-Ы-склеймер.\r\n"
            f"Данный бот является собственностью некого разработчика, не несет никакой персональной и "
            f"прочей ответственности и создан исключительно для сдачи дипломного проекта в Skillbox Python Basic.\r\n"
            f"Приятного просмотра!"
        )


async def get_macbook_info(message: Message, bot: Bot):
    user = await get_user_by_username(message.from_user.username)
    if user:
        await add_request(user, "/macbook")

    async with ChatActionSender.choose_sticker(bot=bot, chat_id=message.from_user.id):
        await asyncio.sleep(1)
        await message.answer(
            f"Отлично, вопрос. Какой вы используете макбук?",
            reply_markup=get_inline_keyboard(),
        )


async def get_cat(message: Message, bot: Bot):
    user = await get_user_by_username(message.from_user.username)
    if user is None:
        await message.answer("Пользователь не найден.")

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with ChatActionSender.choose_sticker(bot=bot, chat_id=message.from_user.id):
        await asyncio.sleep(1)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://catfact.ninja/fact", ssl=ssl_context
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    fact = data["fact"]
                    translator = Translator()
                    translated_fact = translator.translate(fact, dest="ru").text
                    await message.answer(
                        f"Оригинальный текст был:\n\n{fact}.\n\n\nНо после перевода с помощью Translator от компании Google:\n"
                    )
                    await message.answer(translated_fact)
                else:
                    await message.answer(
                        "Не удалось получить факт о кошках. Попробуйте позже."
                    )


async def get_name(message: Message, state: FSMContext, bot: Bot):
    user = await get_user_by_username(message.from_user.username)
    if user:
        await add_request(user, "Начал ввод имени")

    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        await asyncio.sleep(1)
        await message.answer("Введите имя:")
        await state.set_state(StepsForm.GET_NAME)


async def check_name(message: Message, state: FSMContext, bot: Bot):
    user = await get_user_by_username(message.from_user.username)
    if user:
        await add_request(user, f"Введено имя: {message.text}")
    async with ChatActionSender.record_video_note(
        bot=bot, chat_id=message.from_user.id
    ):
        await asyncio.sleep(1)
        await message.answer(
            f"Серьезно? {message.text}????\nЛадно, пусть будет так. Оставляем?\n(Да | yes | нет | no) :)"
        )
        await state.update_data(name=message.text)
        await state.set_state(StepsForm.GET_ANSWER)


async def get_answer(message: Message, state: FSMContext, bot: Bot):
    async with ChatActionSender.choose_sticker(bot=bot, chat_id=message.from_user.id):
        await asyncio.sleep(1)
        if message.text.lower() in ["да", "yes"]:
            user = await get_user_by_username(message.from_user.username)
            if user:
                await add_request(user, f"Подтверждено имя: {message.text}")
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            state_data = await state.get_data()
            name = state_data.get("name")
            if not is_russian_word(name):
                transliterated_name = name
            else:
                transliterated_name = translit(name, reversed=True)
            url = f"https://api.agify.io/?name={transliterated_name}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, ssl=ssl_context) as response:
                    if response.status == 200:
                        data = await response.json()
                        age = data.get("age", "неизвестен")
                        if age is not None and age != "none":
                            await message.answer(
                                f"Возраст для имени {name}: {age} лет."
                            )
                        else:
                            await message.answer(
                                f"Не получается определить возраст для {name}."
                            )
                    else:
                        await message.answer(
                            "Не удалось получить данные. Попробуйте позже или другое имя."
                        )
        else:
            user = await get_user_by_username(message.from_user.username)
            if user:
                await add_request(user, f"Имя: {message.text} не подтверждено.")
            await message.answer("Ну нет так нет. Goodbye!")
        await state.clear()


async def get_requests(message: Message, bot: Bot):
    user = await get_user_by_username(message.from_user.username)
    if user:
        requests = await get_user_requests(user)
        if requests:
            response = "Ваши запросы:\n"
            for req in requests:
                response += f"- {req.request_text} (время: {req.request_time})\n"
        else:
            response = "У вас пока нет сохранённых запросов."
    else:
        response = "Пользователь не найден."
    await message.answer(response)


async def get_echo(message: Message, bot: Bot):
    user = await get_user_by_username(message.from_user.username)
    if user:
        await add_request(user, message.text)

    async with ChatActionSender.upload_voice(bot=bot, chat_id=message.from_user.id):
        await asyncio.sleep(1)
        await message.answer(f"Я вас ни па ни ма ю. Выбериту лучше 1 из команд :)")
