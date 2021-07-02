from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
import clickhouse_driver as ch


class ClickhouseMiddleware(BaseMiddleware):
    def __init__(self, clickhouse_driver: ch.Client):
        self._clickhouse = clickhouse_driver
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        data["clickhouse"] = self._clickhouse
