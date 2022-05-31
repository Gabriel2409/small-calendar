from app.config import get_settings
from app.routers import availabilities, hello
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


def create_app():
    """Creates the fastapi application."""
    app = FastAPI()
    app.include_router(hello.router)
    app.include_router(availabilities.router)
    return app


def init_db(app: FastAPI):
    """Initializes the database. Schemas MUST be generated prior to the connection.

    Note that add_exception_handlers is set to true, which means that each time an
    error occurs in the db, it will be caught by fastapi and return the
    correct status code
    Args:
        app (FastAPI): the fastapi app"""
    db_url = get_settings().database_url
    register_tortoise(
        app,
        db_url=db_url,
        modules={"models": ["app.models.tortoise_models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
