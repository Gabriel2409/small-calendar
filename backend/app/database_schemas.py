import logging
import os

from dotenv import load_dotenv
from tortoise import Tortoise, run_async

log = logging.getLogger("uvicorn")
load_dotenv()

# migrations with aerich
# call aerich init-db on first install and aerich migrate each time the models change
# call aerich upgrade to update the db
TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["app.models.tortoise_models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def generate_schema(db_url: str):
    """Generates the schemas for the database.
    The database is created empty.

    NOTE: it is better to use to cmd line aerich init-db instead to create the db
    and the first migration. However, if you do not care about migrations, you can just
    run this script.

    Note that the schema must be generated before launching the app

    Args:
        db_url(str): the url of the db where we want to generate the schemas

    """
    log.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["models.tortoise_models"]},
    )
    log.info("Generating database schema via Tortoise")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema(db_url=os.environ.get("DATABASE_URL", "")))
