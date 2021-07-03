from aiogram import types
from pydantic import BaseModel


class MainKeyboardButtonsText(BaseModel):
    get_last_articles: str = "Получить последние статьи"


def get_main_keyboard() -> types.ReplyKeyboardMarkup:
    text = MainKeyboardButtonsText()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(text.get_last_articles)

    return keyboard
