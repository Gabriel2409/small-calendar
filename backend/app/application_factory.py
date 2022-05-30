from app.routers import hello
from fastapi import FastAPI


def create_app():
    """Creates the fastapi application."""
    app = FastAPI()
    app.include_router(hello.router)
    return app


def init_db(app: FastAPI):
    """Initializes the database. Schemas MUST be generated prior to the connection.

    Note that add_exception_handlers is set to true, which means that each time an
    error occurs in the db, it will be caught by fastapi and return the
    correct status code
    Args:
        app (FastAPI): the fastapi app"""
    pass
