from aiogram import Dispatcher
import clickhouse_driver as ch

from bot.middlewares.clickhouse import ClickhouseMiddleware


def setup_middlewares(dp: Dispatcher,
                      clickhouse_driver: ch.Client):
    dp.setup_middleware(ClickhouseMiddleware(clickhouse_driver))
