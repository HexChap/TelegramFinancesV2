import aiogram

import TFinances.handlers

from TFinances.core import dispatcher, logger, set_middlewares
from TFinances.core.utilities import configure_db


async def on_startup(dp: aiogram.Dispatcher):
    set_middlewares()
    await configure_db()

    # logger.debug(f"Handlers: {[handler.handler.__name__ for handler in dp.message_handlers.handlers]}")
    logger.debug(f"{len(dp.message_handlers.handlers)} handlers found")

    logger.info(f"({dp.bot.id}) The bot is online.")


if __name__ == '__main__':
    aiogram.executor.start_polling(dispatcher, on_startup=on_startup)
