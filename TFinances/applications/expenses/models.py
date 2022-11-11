from typing import TYPE_CHECKING

from tortoise import fields

from TFinances.core.bases import AbstractModel

if TYPE_CHECKING:
    from ..category import Category
    from ..user import User


class Expense(AbstractModel):
    price = fields.FloatField()
    note = fields.CharField(max_length=64)

    category: fields.ForeignKeyRelation["Category"] = fields.ForeignKeyField(
        "models.Category", related_name="expenses"
    )
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="expenses"
    )

    class Meta:
        table = "expenses"
