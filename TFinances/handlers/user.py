from TFinances.core import dispatcher, logger
from TFinances.applications.user import UserCRUD, UserSchema

from aiogram import types, filters


@dispatcher.message_handler(commands=["user", "me"])
@dispatcher.message_handler(filters.Text("👨‍ Профиль"))
async def me(msg: types.Message, is_inner: bool = False):
    t_id = msg.from_user.id
    user_not_found = f"Creating user with t_id={t_id} because was not found."

    if is_inner:
        logger.debug(user_not_found)

    if not (user := await UserCRUD.get_by_telegram_id(t_id)):
        user = await UserCRUD.create_by(
            UserSchema(
                telegram_id=t_id,
                lang=msg.from_user.language_code
            )
        )
        logger.debug(user_not_found)

    await msg.reply(
        f"💼 Hello, {msg.from_user.first_name}!\n\n"
        f"⚰ Telegram ID: {t_id}\n"
        f"🪪 Internal ID: {user.id}"
    )

    return user
