import logging as log
from enum import Enum
from typing import Optional

from pydantic import BaseSettings
from urlpath import URL

# Edit this!
PARSE_MODE = "HTML"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


class UpdateMethod(str, Enum):
    WEBHOOKS = "webhooks"
    LONG_POLLING = "long_polling"


class LogLevel(int, Enum):
    CRITICAL = log.CRITICAL
    FATAL = log.FATAL
    ERROR = log.ERROR
    WARNING = log.WARNING
    WARN = log.WARN
    INFO = log.INFO
    DEBUG = log.DEBUG


class Config(BaseSettings):
    tg_token: str
    tg_admins_id: str
    tg_webhook_host: Optional[str]
    tg_webhook_path: str = "/bot"

    webapp_host: str = "localhost"
    webapp_port: int = 3000

    log_level: LogLevel = LogLevel.INFO

    clickhouse_host: str = "localhost"
    clickhouse_port: Optional[str]
    clickhouse_database: str = "habra_reader"
    clickhouse_user: str = "default"
    clickhouse_password: str = ""

    @property
    def tg_update_method(self) -> UpdateMethod:
        return UpdateMethod.LONG_POLLING if not self.tg_webhook_host else UpdateMethod.WEBHOOKS

    @property
    def tg_webhook_url(self) -> str:
        return str(URL(self.tg_webhook_host, self.tg_webhook_path))

    @property
    def tg_parse_mode(self) -> str:
        # PARSE_MODE must be specified in the code, because the way
        # the message is parsed directly affects the code
        return PARSE_MODE

    @property
    def log_format(self):
        # LOG_FORMAT must be specified in the code,
        # because The format depends on the logging library used
        return LOG_FORMAT


config = Config(
    _env_file=".env",
    _env_file_encoding="utf-8"
)
