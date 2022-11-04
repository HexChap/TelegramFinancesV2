from tortoise import fields

from TFinances.core import AbstractModel


class User(AbstractModel):
    telegram_id = fields.BigIntField(unique=True)
    lang = fields.TextField()

    class Meta:
        table = "users"
