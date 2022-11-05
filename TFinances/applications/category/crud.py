from typing import TYPE_CHECKING

from TFinances.core.bases import BaseCRUD
from . import Category, CategorySchema

if TYPE_CHECKING:
    from ..user import User


class CategoryCRUD(BaseCRUD):
    model = Category

    @classmethod
    async def create(cls, payload: CategorySchema) -> Category:
        return await cls.model.create(**payload.dict())

    @classmethod
    async def get_by_user(cls, user: "User") -> list[Category]:
        return await cls.filter_by(user_id=user.id)
