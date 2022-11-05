from aiogram import types, filters
from aiogram.dispatcher import FSMContext

from TFinances.core import dispatcher, logger
from .user import me


@dispatcher.message_handler(commands=["start"])
async def start(msg: types.Message):
    logger.debug(f'"start" handler entry.')

    await me(msg)


@dispatcher.message_handler(commands='cancel', state='*')
@dispatcher.message_handler(filters.Text(equals="🏠 Back to menu."), state="*")
async def cancel(message: types.Message, state: FSMContext, is_inner: bool = False):
    """
    Cancels every active state.
    """
    logger.debug('"cancel" handler entry.')

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    logger.debug(f"{state} was cancelled.")

    if not is_inner:
        await message.reply("✅ Action cancelled.", reply_markup=types.ReplyKeyboardRemove())
