from TFinances.core import dispatcher, logger
from TFinances.applications.user import UserCRUD, UserSchema

from aiogram import types, filters


@dispatcher.message_handler(commands=["user", "me"])
@dispatcher.message_handler(filters.Text("👨‍ Профиль"))
async def me(msg: types.Message):
    logger.debug('"me" handler entry.')
    user_id = msg.from_user.id

    if not (user := await UserCRUD.get_by_telegram_id(user_id)):
        user = await UserCRUD.create(
            UserSchema(
                telegram_id=user_id,
                lang=msg.from_user.language_code
            )
        )
        logger.debug(f"User ({user_id}) was not found so it was created.")

    await msg.reply(
        f"💼 Hello, {msg.from_user.first_name}!\n\n"
        f"⚰ Telegram ID: {user_id}\n"
        f"🪪 ID: {user.id}"
    )
