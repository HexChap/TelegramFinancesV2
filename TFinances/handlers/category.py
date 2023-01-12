import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from TFinances.core import dispatcher, logger
from TFinances.core.bases import create_reply_keyboard_by
from TFinances.applications.category import CategoryCRUD, states, CategorySchema
from TFinances.applications.user import UserCRUD
from .user import me

C_NAME_PATTERN = re.compile(r"^.{2,16}$")
C_DESC_PATTERN = re.compile(r"^.{2,120}$")


# region add_category
@dispatcher.message_handler(state="*", commands=["add_category"])
async def add_category(msg: types.Message):
    if not (await UserCRUD.get_by_telegram_id(t_id := msg.from_user.id)):

        await me(msg)

    await states.CategorySG.name.set()

    await msg.reply(
        "🪧 Enter the name of the category.\n\n"
        "❗ It must contain at least 2 and no more than 24 characters."
    )


@dispatcher.message_handler(state=states.CategorySG.name)
async def process_name(msg: types.Message, state: FSMContext):
    try:
        await _process_name(msg, state)

    except ValueError as e:
        logger.debug(f"Bad name entered. details=\"{str(e)}\"")
        await msg.reply(str(e))
        return

    await states.CategorySG.description.set()

    await msg.reply(
        "🪧 Write a description for the category.\n\n"
        "❗ It must contain at least 2 and no more than 120 characters.",
        reply_markup=types.ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True
        ).add(
            types.KeyboardButton("⏩ Skip")
        )
    )


@dispatcher.message_handler(state=states.CategorySG.description)
async def process_description_or_skip(msg: types.Message, state: FSMContext):
    if msg.text == "⏩ Skip":
        logger.debug("Description setting was skipped")
        await _finish(msg, state)
        return

    try:
        await _process_description(msg, state)
        logger.debug(f"Description processed successfully -> finish stage")
        await _finish(msg, state)

    except ValueError as e:
        logger.debug(f"Bad description was written")
        await msg.reply(str(e))
        return


async def _process_name(msg: types.Message, state: FSMContext):
    if await CategoryCRUD.get_by(name=msg.text):
        raise ValueError("❌ A category with this name already exists.\n⚙️ Choose another name.")

    if not re.match(C_NAME_PATTERN, msg.text):
        raise ValueError("❌ The category name must contain at least 2 and no more than 16 characters.")

    async with state.proxy() as data:
        data["name"] = msg.text
        logger.debug(f"The data was updated with name={msg.text}.")


async def _process_description(msg: types.Message, state: FSMContext):
    if not re.match(C_DESC_PATTERN, msg.text):
        raise ValueError("❌ The category name must contain at least 2 and no more than 120 characters.")

    async with state.proxy() as data:
        data["description"] = msg.text
        logger.debug(f"The data was updated with {len(msg.text)} characters long description")


async def _finish(msg: types.Message, state: FSMContext):
    user = await UserCRUD.get_by_telegram_id(msg.from_user.id)

    async with state.proxy() as data:
        schema = CategorySchema(
            name=data["name"],
            description=data["description"] if data.get("description", None) else None,
            user_id=user.id
        )

        category = await CategoryCRUD.create_by(schema)
        logger.debug(f"Category *{schema.name}* (category_id={category.id}) for user_id={user.id} created")

    await state.finish()

    await msg.answer(
        f"✅ Category `{schema.name}` created!" +
        (f"\n\nℹ Description: `{schema.description}`" if schema.description else ""),
        reply_markup=types.ReplyKeyboardRemove(),
        parse_mode=types.ParseMode.MARKDOWN
    )


# endregion add_category


# region delete_category
@dispatcher.message_handler(commands="delete_category")
async def delete_category(msg: types.Message):
    if not (user := await UserCRUD.get_by_telegram_id(t_id := msg.from_user.id)):
        logger.debug(f"Creating user with t_id={t_id} because was not found.")
        await me(msg)
        return

    if not (categories := await CategoryCRUD.get_all_by_user_id(user.id)):
        logger.debug(f"No categories found for user with t_id={t_id}. Returning")
        await msg.reply("ℹ️ To begin with, it's worth adding some categories.\n"
                        "📁 A new category can be created using the /add_category command")
        return

    kb = create_reply_keyboard_by([category.name for category in categories])

    await states.ChooseCategorySG.category_name.set()
    await msg.reply(
        " 🗑 Select the category you want to delete.",
        reply_markup=kb
    )


@dispatcher.message_handler(state=states.ChooseCategorySG.category_name)
async def process_category_to_del(msg: types.Message, state: FSMContext):
    if not await CategoryCRUD.get_by(name=msg.text):
        raise ValueError("❌ Category can't be found.\n⌨️ Select a category using the keyboard.")

    await CategoryCRUD.delete_by(name=msg.text)
    await msg.answer(
        f"✅ Category `{msg.text}` was deleted successfully.",
        parse_mode=types.ParseMode.MARKDOWN
    )

    await state.finish()
    logger.debug(f"State closed. chat_id={state.chat}")
# endregion delete_category


# region update_category
@dispatcher.message_handler(commands=["update_category"])
async def update_category(msg: types.Message):
    pass
# endregion update_category
