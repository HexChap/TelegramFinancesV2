from typing import TYPE_CHECKING

from tortoise import fields

from TFinances.core import AbstractModel

if TYPE_CHECKING:
    from ..category.models import Category


class User(AbstractModel):
    telegram_id = fields.BigIntField(unique=True)
    lang = fields.TextField()

    category: fields.ReverseRelation["Category"]

    class Meta:
        table = "users"
