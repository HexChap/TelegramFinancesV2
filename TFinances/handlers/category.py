import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from TFinances.core import dispatcher, logger
from TFinances.applications.category import CategoryCRUD, CategorySG, CategorySchema
from TFinances.applications.user import UserCRUD
from .user import me

C_NAME_PATTERN = re.compile(r"^.{2,16}$")
C_DESC_PATTERN = re.compile(r"^.{2,120}$")


@dispatcher.message_handler(state="*", commands=["add_category"])
async def add_category(msg: types.Message):
    logger.debug('"add_category" handler entry.')
    if not (await UserCRUD.get_by_telegram_id(t_id := msg.from_user.id)):
        logger.debug(f"Creating user with t_id={t_id} because was not found.")
        await me(msg)

    await CategorySG.name.set()

    await msg.reply(
        "🪧 Enter the name of the category.\n"
        "❗ It must contain at least 2 and no more than 24 characters."
    )


@dispatcher.message_handler(state=CategorySG.name)
async def process_name(msg: types.Message, state: FSMContext):
    logger.debug(f"Processing the name. chat_id={state.chat}")
    try:
        await _process_name(msg, state)

    except ValueError as e:
        logger.debug(f"Bad name entered. chat_id={state.chat}")
        await msg.reply(str(e))
        return

    await CategorySG.description.set()

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


@dispatcher.message_handler(state=CategorySG.description)
async def process_description_or_skip(msg: types.Message, state: FSMContext):
    if msg.text == "⏩ Skip":
        logger.debug("The description setting was skipped.")
        await _finish(msg, state)
        return

    try:
        logger.debug(f"Processing description. chat_id={state.chat}")
        await _process_description(msg, state)
        logger.debug(f"Description processed successfully -> finish stage. chat_id={state.chat}")
        await _finish(msg, state)

    except ValueError as e:
        logger.debug(f"Bad description was written. chat_id={state.chat}")
        await msg.reply(str(e))
        return


async def _process_name(msg: types.Message, state: FSMContext):
    if not re.match(C_NAME_PATTERN, msg.text):
        raise ValueError("❌ The category name must contain at least 2 and no more than 16 characters.")

    async with state.proxy() as data:
        data["name"] = msg.text
        logger.debug(f"The data was updated with name={msg.text}. chat_id={state.chat}")


async def _process_description(msg: types.Message, state: FSMContext):
    if not re.match(C_DESC_PATTERN, msg.text):
        raise ValueError("❌ The category name must contain at least 2 and no more than 120 characters.")

    async with state.proxy() as data:
        data["description"] = msg.text
        logger.debug(f"The data was updated with description={msg.text}. chat_id={state.chat}")


async def _finish(msg: types.Message, state: FSMContext):
    user = await UserCRUD.get_by_telegram_id(msg.from_user.id)

    async with state.proxy() as data:
        schema = CategorySchema(
                name=data["name"],
                description=data["description"] if data.get("description", None) else None,
                user_id=user.id
            )

        await CategoryCRUD.create_by(schema)
        logger.debug(f"Category *{schema.name}* created for user_id={user.id}. chat_id={state.chat}")

    await state.finish()
    logger.debug(f"State closed. chat_id={state.chat}")

    await msg.answer(
        f"✅ Category `{schema.name}` created!" +
        (f"\n\nℹ Description: `{schema.description}`" if schema.description else "")
    )
