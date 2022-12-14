import asyncio
import sys
from pathlib import Path

from loguru import logger
from pydantic import BaseSettings, BaseModel
from aiogram import Bot, Dispatcher
from aiogram.types.message import ParseMode
from aiogram.contrib.fsm_storage.files import MemoryStorage


class Database(BaseSettings):
    address: str
    port: int
    db_name: str
    user: str
    password: str


class Tokens(BaseSettings):
    exchange_api_token: str
    token: str


class Misc(BaseSettings):
    owner_id: int
    logger_level: str


class Settings(BaseModel):
    database: Database
    tokens: Tokens
    misc: Misc


_envs_path = Path(".envs")
_database = Database(_env_file=_envs_path / "database.env", _env_file_encoding="utf-8")
_tokens = Tokens(_env_file=_envs_path / "tokens.env", _env_file_encoding="utf-8")
_misc = Misc(_env_file=_envs_path / "misc.env", _env_file_encoding="utf-8")

settings = Settings(
    database=_database,
    tokens=_tokens,
    misc=_misc
)
bot = Bot(token=settings.tokens.token)
storage = MemoryStorage()
dispatcher = Dispatcher(bot, loop=asyncio.get_event_loop(), storage=storage)

if (level := settings.misc.logger_level) != "DEBUG":
    logger.remove()
    logger.add(sys.stderr, level=level)
