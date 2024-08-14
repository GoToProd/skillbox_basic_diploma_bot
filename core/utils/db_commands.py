import asyncio
from core.utils.models import User, Request


async def add_user(user_name: str, first_name: str):
    user = await asyncio.get_event_loop().run_in_executor(
        None, lambda: User.create(user_name=user_name, first_name=first_name)
    )
    return user


async def add_request(user: User, request_text: str):
    request = await asyncio.get_event_loop().run_in_executor(
        None, lambda: Request.create(user=user, request_text=request_text)
    )
    return request


async def get_user_by_username(username: str):
    loop = asyncio.get_event_loop()
    user = await loop.run_in_executor(
        None, lambda: User.get_or_none(User.user_name == username)
    )
    return user


async def get_user_requests(user):
    loop = asyncio.get_event_loop()
    requests = await loop.run_in_executor(
        None, lambda: list(Request.select().where(Request.user == user))
    )
    return requests
