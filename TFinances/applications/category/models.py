from typing import TYPE_CHECKING

from tortoise import fields

from TFinances.core.bases import AbstractModel

if TYPE_CHECKING:
    from ..user.models import User


class Category(AbstractModel):
    name = fields.CharField(max_length=16)
    description = fields.CharField(max_length=120, null=True)

    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="categories"
    )

    class Meta:
        table = "categories"
