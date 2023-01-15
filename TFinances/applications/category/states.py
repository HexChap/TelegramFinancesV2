from aiogram.dispatcher.filters.state import State, StatesGroup


class CategoryUpdateSG(StatesGroup):
    name = State()
    description = State()


class CategorySG(StatesGroup):
    name = State()
    description = State()


class ChooseCategoryDelSG(StatesGroup):
    category_name = State()


class ChooseCategoryUpdSG(StatesGroup):
    category_name = State()
