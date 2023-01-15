from typing import Iterable

from aiogram import types

skip_kb = types.ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True
).add(
    types.KeyboardButton("⏩ Skip")
)


def create_reply_keyboard_by(iterable: Iterable) -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    for item in iterable:
        kb.add(types.KeyboardButton(str(item)))

    return kb
