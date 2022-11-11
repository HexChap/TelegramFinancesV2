from .models import User
from .schemas import UserSchema
from ...core.bases import BaseCRUD


class UserCRUD(BaseCRUD):
    model = User

    @classmethod
    async def get_by_id(cls, id: int) -> User:
        return await cls.get_by(id=id)
    
    @classmethod
    async def get_by_telegram_id(cls, telegram_id: int) -> User | None:
        return await cls.get_by(telegram_id=telegram_id)

    @classmethod
    async def update(cls, payload: UserSchema) -> User:
        return await cls.update_by(payload, telegram_id=payload.telegram_id)

    @classmethod
    async def delete(cls, telegram_id: int):
        await cls.delete_by(telegram_id=telegram_id)
