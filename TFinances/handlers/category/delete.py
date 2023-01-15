from aiogram import types
from aiogram.dispatcher import FSMContext

from TFinances.applications.category import CategoryCRUD, states
from TFinances.core import dispatcher, logger
from .update import choose_category


@dispatcher.message_handler(commands=["delete_category"])
async def delete_category(msg: types.Message):
    await choose_category(msg, is_for_deletion=True)


@dispatcher.message_handler(state=states.ChooseCategoryDelSG.category_name)
async def process_category_del(msg: types.Message, state: FSMContext):
    if not (category := await CategoryCRUD.get_by(name=msg.text)):
        await msg.reply("❌ Category can't be found.\n⌨️ Select a category using the keyboard.")
        return

    logger.debug(f"Deleting {str(category)} id={category.id}")
    await category.delete()  # Saves one query to the database

    await msg.answer(
        f"✅ Category `{msg.text}` was deleted successfully.",
        parse_mode=types.ParseMode.MARKDOWN
    )

    await state.finish()


# endregion delete_category
