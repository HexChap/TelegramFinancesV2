from aiogram import types
from aiogram.dispatcher import FSMContext

from TFinances.applications.category import CategoryCRUD, states, CategorySchema
from TFinances.applications.user import UserCRUD
from TFinances.core import dispatcher, logger
from TFinances.core.keyboards import create_reply_keyboard_by, skip_kb
from .add import validate_category_name, validate_category_description


async def choose_category(msg: types.Message, is_for_deletion: bool = False):
    user = await UserCRUD.get_by_telegram_id(t_id := msg.from_user.id)

    if not (categories := await CategoryCRUD.get_all_by_user_id(user.id)):
        logger.debug(f"No categories found for user with t_id={t_id}. Returning")
        await msg.reply("ℹ️ To begin with, it's worth adding some categories.\n\n"
                        "📁 A new category can be created using the /add_category command")
        return

    kb = create_reply_keyboard_by([category.name for category in categories])

    if is_for_deletion:
        await states.ChooseCategoryDelSG.category_name.set()
    else:
        await states.ChooseCategoryUpdSG.category_name.set()

    await msg.answer(
        " 🗂 Select а category.",
        reply_markup=kb
    )


@dispatcher.message_handler(commands=["update_category"])
async def update_category(msg: types.Message):
    await choose_category(msg)


@dispatcher.message_handler(state=states.ChooseCategoryUpdSG.category_name)
async def process_category_update(msg: types.Message, state: FSMContext):
    if not (category := await CategoryCRUD.get_by(name=msg.text)):
        await msg.reply("❌ Category can't be found.\n⌨️ Select a category using the keyboard.")
        return

    async with state.proxy() as data:
        data.update(category=category)

    await msg.answer(
        "🪧 Enter a new name for the category.\n\n"
        "❗ It must contain at least 2 and no more than 24 characters.",
        reply_markup=skip_kb
    )
    await states.CategoryUpdateSG.name.set()


@dispatcher.message_handler(state=states.CategoryUpdateSG.name)
async def process_name(msg: types.Message, state: FSMContext):
    if not msg.text == "⏩ Skip":

        try:
            await validate_category_name(msg, state)

        except ValueError as e:
            logger.debug(f"Bad name entered.")
            await msg.reply(str(e))
            return

    await states.CategoryUpdateSG.description.set()
    await msg.answer(
        "🪧 Write new description for the category.\n\n"
        "❗ It must contain at least 2 and no more than 120 characters.",
        reply_markup=skip_kb
    )


@dispatcher.message_handler(state=states.CategoryUpdateSG.description)
async def process_description(msg: types.Message, state: FSMContext):
    if not msg.text == "⏩ Skip":

        try:
            await validate_category_description(msg, state)

        except ValueError as e:
            logger.debug(f"Bad description was written")
            await msg.reply(str(e))
            return

    await _finish_update(msg, state)


async def _finish_update(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if len(data.values()) == 1:  # There is only an instance of the category
            await msg.answer("🤧 Nothing to update.")
            await state.finish()
            return

        schema = CategorySchema(
            name=data.get("name", None),
            description=data.get("description", None),
            user_id=None
        )

        await CategoryCRUD.update_by(schema, id=data.get("category").id)

    await state.finish()

    await msg.answer(
        "✅ Category successfully updated."
    )
