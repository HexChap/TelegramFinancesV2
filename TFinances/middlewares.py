from aiogram import Dispatcher, types
from aiogram.dispatcher.handler import current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware

from TFinances.applications import UserCRUD
from TFinances.core import logger
from TFinances.handlers import me


class HandlerMiddleware(BaseMiddleware):
    async def on_process_message(self, msg: types.Message, __):
        handler = current_handler.get()

        if not (await UserCRUD.get_by_telegram_id(t_id := msg.from_user.id)):
            logger.debug(f"Creating user with t_id={t_id} because was not found.")
            await me(msg, is_inner=True)
            return

        if any(states := await self._get_states(handler)) \
                and not (['*'] == states):
            logger.debug(f"Processing: {', '.join(states)}")
        else:
            logger.debug(f"`{handler.__name__}` handler entry")

    @staticmethod
    async def _get_states(handler: callable) -> list:
        dp = Dispatcher.get_current()
        msg_handlers = dp.message_handlers.handlers

        handler_index = [
            handler_obj.handler.__name__
            for handler_obj in msg_handlers
        ].index(handler.__name__)

        return msg_handlers[handler_index].filters[0].filter.states


MIDDLEWARES = [
    LogMiddleware
]


def set_middlewares():
    dp = Dispatcher.get_current()

    [dp.middleware.setup(middleware()) for middleware in MIDDLEWARES]
