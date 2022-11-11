from typing import TYPE_CHECKING

from TFinances.core.bases import BaseCRUD
from . import Category, CategorySchema

if TYPE_CHECKING:
    from ..user import User


class CategoryCRUD(BaseCRUD):
    model = Category

    @classmethod
    async def get_all_by_user(cls, user: "User") -> list[Category]:
        return await cls.filter_by(user_id=user.id)
