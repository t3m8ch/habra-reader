import aiohttp
import clickhouse_driver as ch
from aiogram import types
from aiogram.dispatcher.filters import Text

from bot.keyboards import get_main_keyboard, MainKeyboardButtonsText
from bot.misc import Router
from bot.services.habr import HabraService

router = Router()


@router.message(commands=["new"])
@router.message(Text(equals=MainKeyboardButtonsText().get_last_articles))
async def cmd_new(message: types.Message, clickhouse: ch.Client):
    async with aiohttp.ClientSession() as session:
        habra_service = HabraService(session, clickhouse)
        articles = await habra_service.get_last_articles()

        if not articles:
            await message.answer("Новых статей пока нет :(")
            return

        for i, a in enumerate(articles):
            text = f"<b>{a.title}</b>\n\n" \
                   f"{a.description}\n\n" \
                   f"{a.url}"
            if i == len(articles) - 1:
                await message.answer(text, reply_markup=get_main_keyboard())
            else:
                await message.answer(text)
