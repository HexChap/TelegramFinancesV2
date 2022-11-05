import aiogram

import TFinances.handlers

from TFinances.core import dispatcher, logger
from TFinances.core.utilities import configure_db


async def on_startup(dp: aiogram.Dispatcher):
    await configure_db()

    logger.debug(f"Handlers: {[handler.handler.__name__ for handler in dp.message_handlers.handlers]}")
    logger.info(f"({dp.bot.id}) The bot is online.")


if __name__ == '__main__':
    aiogram.executor.start_polling(dispatcher, on_startup=on_startup)
