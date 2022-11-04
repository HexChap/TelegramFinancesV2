import aiogram

import handlers

from TFinances.core.settings import dispatcher


async def on_startup(dp: aiogram.Dispatcher):
    print("\nBot online \n-----------")


if __name__ == '__main__':
    aiogram.executor.start_polling(dispatcher, on_startup=on_startup)
