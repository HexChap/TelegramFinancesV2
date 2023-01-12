from TFinances.core.bases import BaseCRUD
from . import Category


class CategoryCRUD(BaseCRUD):
    model = Category

    @classmethod
    async def get_all_by_user_id(cls, user_id: int) -> list[Category]:
        return await cls.filter_by(user_id=user_id)
