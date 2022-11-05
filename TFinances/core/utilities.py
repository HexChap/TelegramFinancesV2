import os
from pathlib import Path

from tortoise import Tortoise

from TFinances.applications.category import CategoryCRUD, CategorySchema
from TFinances.applications.user import UserCRUD
from TFinances.applications.user.schemas import UserSchema
from TFinances.core.settings import settings, logger

db = settings.database
DB_URL = (
    "postgres://"
    f"{db.user}:{db.password}@"
    f"{db.address}:{db.port}/{db.db_name}"
)


async def configure_db():
    models = [
        f'TFinances.applications.{app_dir}.models'
        for app_dir in os.listdir(Path("TFinances") / "applications")
        if not app_dir.startswith("_")
    ]
    logger.debug(f"Found models: {models}")

    await Tortoise.init(db_url=DB_URL, modules={"models": models})
    logger.debug("Tortoise initialized.")

    await Tortoise.generate_schemas()
    logger.debug("Schemas generated.")


# async def test():
#     print(
#         (
#             await UserCRUD.create(
#                 UserSchema(
#                     telegram_id=1370280956,
#                     lang="ruRU"
#                 )
#             )
#         ).lang
#     )
#     print(
#         (
#             await UserCRUD.get_by_telegram_id(1370280956)
#         ).lang
#     )
#     print(
#         (
#             await UserCRUD.update(
#                 UserSchema(
#                     telegram_id=1370280956,
#                     lang="usUS"
#                 )
#             )
#         ).lang
#     )
#     print(
#         await UserCRUD.delete(1370280956)
#     )
# async def test():
#     await UserCRUD.create(UserSchema(telegram_id=1370280956, lang="enUS"))
#     await CategoryCRUD.create(
#         CategorySchema(
#             name="a1",
#             description="asd",
#             user_id=1
#         )
#     )
#     await CategoryCRUD.create(
#         CategorySchema(
#             name="a2",
#             description="asdasd",
#             user_id=1
#         )
#     )
#     await CategoryCRUD.create(
#         CategorySchema(
#             name="a3",
#             description="asdasdasd",
#             user_id=1
#         )
#     )
#     await CategoryCRUD.create(
#         CategorySchema(
#             name="a4",
#             description="asdasdasdasd",
#             user_id=1
#         )
#     )
#
#     user = await UserCRUD.get_by_telegram_id(1370280956)
#     print(
#         (
#             await CategoryCRUD.get_by_user(user)
#         )
#     )
#     print(
#         (
#             await CategoryCRUD.update_by(
#                 CategorySchema(
#                     name="test",
#                     description="testdesc",
#                     user_id=None
#                 ),
#                 id=2
#             )
#         )
#     )