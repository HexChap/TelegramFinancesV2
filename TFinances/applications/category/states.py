from aiogram.dispatcher.filters.state import State, StatesGroup


class CategorySG(StatesGroup):
    name = State()
    description = State()


class ChooseCategorySG(StatesGroup):
    category_name = State()
