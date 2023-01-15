from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from pydantic import BaseModel
from tortoise import Model, fields
from tortoise.exceptions import DoesNotExist

from TFinances.core.settings import logger


class AbstractModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True


class BaseCRUD:
    model: Model

    @classmethod
    async def create_by(cls, payload: BaseModel) -> "model":
        instance = await cls.model.create(**payload.dict())

        logger.debug(f"New {str(instance)} id={instance.id} was created.")

        return instance

    @classmethod
    async def get_by(cls, **kwargs) -> "model":
        logger.debug(f"Getting `{cls.model.__name__}` by {kwargs}")
        try:
            return await cls.model.get_or_none(**kwargs)

        except DoesNotExist as e:
            logger.error(e)
            raise e

    @classmethod
    async def filter_by(cls, **kwargs) -> list["model"]:
        logger.debug(f"Filtering {cls.model.__name__} instances by {kwargs}")
        try:
            return await cls.model.filter(**kwargs)

        except DoesNotExist as e:
            logger.error(e)
            raise e

    @classmethod
    async def update_by(cls, payload: BaseModel, **kwargs) -> "model":
        instance = await cls.get_by(**kwargs)

        await instance.update_from_dict(
            {
                key: value for key, value in payload.dict().items()
                if value is not None
            }
        ).save()
        logger.debug(f"{str(instance)} id={instance.id} was updated.")

        return instance

    @classmethod
    async def delete_by(cls, **kwargs) -> None:
        instance = await cls.get_by(**kwargs)

        logger.debug(f"Deleting {str(instance)} id={instance.id}")

        await instance.delete()

