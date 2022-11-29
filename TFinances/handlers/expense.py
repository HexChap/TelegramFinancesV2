from aiogram import types

from TFinances.core import dispatcher, logger
from TFinances.applications import UserCRUD, ExpenseCRUD, CategoryCRUD
from .user import me


@dispatcher.message_handler(commands=["expenses"])
async def my_expenses(msg: types.Message):
    resp = "📑 All wastes\n\n"

    if not (user := await UserCRUD.get_by_telegram_id(msg.from_user.id)):
        user = await me(msg)

    expenses = await ExpenseCRUD.get_all_by(user_id=user.id)
    user_cats = await CategoryCRUD.filter_by(user_id=user.id)

    for category in user_cats:
        total = sum(
            [
                expense.price
                for expense in filter(lambda e: e.category_id == category.id, expenses)
            ]
        )
        resp += f"    ‣  *{category.name}:* `{total}`\n"

    await msg.reply(resp)


@dispatcher.message_handler(commands=["delete_expense"])
async def delete_expense(msg: types.Message):
    pass
