import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from TFinances.applications.category import CategoryCRUD, states, CategorySchema
from TFinances.applications.user import UserCRUD
from TFinances.core import dispatcher, logger
from TFinances.core.keyboards import skip_kb

C_NAME_PATTERN = re.compile(r"^.{2,16}$")
C_DESC_PATTERN = re.compile(r"^.{2,120}$")


@dispatcher.message_handler(commands=["add_category"])
async def add_category(msg: types.Message):
    await states.CategorySG.name.set()

    await msg.answer(
        "🪧 Enter the name of the category.\n\n"
        "❗ It must contain at least 2 and no more than 24 characters."
    )


@dispatcher.message_handler(state=states.CategorySG.name)
async def process_name(msg: types.Message, state: FSMContext):
    try:
        await validate_category_name(msg, state)

    except ValueError as e:
        logger.debug(f"Bad name entered.")
        await msg.reply(str(e))
        return

    await states.CategorySG.description.set()

    await msg.answer(
        "🪧 Write a description for the category.\n\n"
        "❗ It must contain at least 2 and no more than 120 characters.",
        reply_markup=skip_kb
    )


@dispatcher.message_handler(state=states.CategorySG.description)
async def process_description_or_skip(msg: types.Message, state: FSMContext):
    if msg.text == "⏩ Skip":
        logger.debug("Description setting was skipped")
        await _finish(msg, state)
        return

    try:
        await validate_category_description(msg, state)
        logger.debug(f"Description processed successfully -> finish stage")

    except ValueError as e:
        logger.debug(f"Bad description was written")
        await msg.answer(str(e))
        return

    await _finish(msg, state)


async def validate_category_name(msg: types.Message, state: FSMContext):
    if await CategoryCRUD.get_by(name=msg.text):
        raise ValueError("❌ A category with this name already exists.\n⚙️ Choose another name.")

    if not re.match(C_NAME_PATTERN, msg.text):
        raise ValueError("❌ The category name must contain at least 2 and no more than 16 characters.")

    async with state.proxy() as data:
        data["name"] = msg.text
        logger.debug(f"The data was updated with name={msg.text}.")


async def validate_category_description(msg: types.Message, state: FSMContext):
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

        await CategoryCRUD.create_by(schema)

    await state.finish()

    await msg.answer(
        f"✅ Category `{schema.name}` created!" +
        (f"\n\nℹ Description: `{schema.description}`" if schema.description else ""),
        reply_markup=types.ReplyKeyboardRemove(),
        parse_mode=types.ParseMode.MARKDOWN
    )
