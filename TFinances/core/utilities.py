import os
from pathlib import Path

from tortoise import Tortoise

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
