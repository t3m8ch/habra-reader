import aiohttp
import clickhouse_driver as ch
from aiogram import types

from bot.misc import Router
from bot.services.habr import HabraService

router = Router()


@router.message(commands=["new"])
async def cmd_new(message: types.Message, clickhouse: ch.Client):
    async with aiohttp.ClientSession() as session:
        habra_service = HabraService(session, clickhouse)
        articles = await habra_service.get_new_articles()

        if not articles:
            await message.answer("Новых статей пока нет :(")
            return

        for a in articles:
            text = f"<b>{a.title}</b>\n\n" \
                   f"{a.description}\n\n" \
                   f"{a.url}"
            await message.answer(text)
