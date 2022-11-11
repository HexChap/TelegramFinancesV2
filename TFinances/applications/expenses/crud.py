from TFinances.core.bases import BaseCRUD
from . import Expense, ExpenseSchema


class ExpenseCRUD(BaseCRUD):
    model = Expense

    @classmethod
    async def get_all_by(cls, **kwargs) -> list[Expense]:
        """

        :param kwargs: user_id or category_id
        :return: ORM Expense instance
        """
        if not (kwargs.get("category_id") or kwargs.get("user_id")):
            raise ValueError("The keyword argument must be with key *category_id* or *user_id*.")

        return await cls.filter_by(**kwargs)
