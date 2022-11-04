import aiogram

import handlers

from TFinances.core.settings import dispatcher, logger
from TFinances.core.utilities import configure_db


async def on_startup(dp: aiogram.Dispatcher):
    await configure_db()

    logger.info(f"({dp.bot.id}) The bot is online.")


if __name__ == '__main__':
    aiogram.executor.start_polling(dispatcher, on_startup=on_startup)
