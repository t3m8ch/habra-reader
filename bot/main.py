import asyncio
import logging as log

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import clickhouse_driver as ch

from bot.middlewares import setup_middlewares
from config import config, UpdateMethod
from handlers import register_handlers


async def on_startup(dp: Dispatcher):
    if config.tg_update_method == UpdateMethod.WEBHOOKS:
        await dp.bot.set_webhook(config.tg_webhook_url)

    log.warning("START BOT!")


async def on_shutdown(dp: Dispatcher):
    await dp.bot.delete_webhook()

    await dp.storage.close()
    await dp.storage.wait_closed()

    log.warning("BOT STOPPED!")


def init_db(clickhouse: ch.Client):
    clickhouse.execute(
        "CREATE TABLE IF NOT EXISTS article ( "
        "`date_added` Date DEFAULT now(), "
        "`title` String, "
        "`description` String, "
        "`url` String ) "
        "ENGINE = ReplacingMergeTree() "
        "ORDER BY (date_added, title)"
    )


def run():
    # Logging configuration
    log.basicConfig(
        level=config.log_level,
        format=config.log_format
    )

    # Base
    event_loop = asyncio.get_event_loop()
    storage = MemoryStorage()  # TODO: Redis
    bot = Bot(
        token=config.tg_token,
        parse_mode=config.tg_parse_mode
    )
    dp = Dispatcher(bot, storage=storage)

    # DB
    clickhouse = ch.Client(
        host=config.clickhouse_host,
        port=config.clickhouse_port,
        database=config.clickhouse_database,
        user=config.clickhouse_user,
        password=config.clickhouse_password
    )
    init_db(clickhouse)

    # Register
    register_handlers(dp)
    setup_middlewares(dp, clickhouse)

    # Start bot!
    if config.tg_update_method == UpdateMethod.LONG_POLLING:
        executor.start_polling(
            dispatcher=dp,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            loop=event_loop,
            skip_updates=True
        )

    elif config.tg_update_method == UpdateMethod.WEBHOOKS:
        executor.start_webhook(
            dispatcher=dp,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            loop=event_loop,
            webhook_path=config.tg_webhook_path,
            host=config.webapp_host,
            port=config.webapp_port,
            skip_updates=True
        )


if __name__ == "__main__":
    run()
