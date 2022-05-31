import pathlib

import pytest
from app.application_factory import create_app
from app.config import Settings, get_settings
from app.models.tortoise_models import AvailabilitiesModel, ReservationsModel
from fastapi.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

db_path = "sql_test.sqlite3"
test_db_url = f"sqlite://{db_path}"


def get_settings_override() -> Settings:
    """Overrides the settings for testing

    Returns:
        Settings: fastapi test settings
    """
    return Settings(env="testing", database_url=test_db_url)


@pytest.fixture(scope="module")
def test_app():
    """test client"""
    # set up
    app = create_app()
    app.dependency_overrides[get_settings] = get_settings_override

    # test db
    register_tortoise(
        app,
        db_url=test_db_url,
        modules={"models": ["app.models.tortoise_models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )

    # testing
    with TestClient(app) as test_client:
        yield test_client

    # tear down
    # ugly way to remove the test db
    pathlib.Path(db_path).unlink()


@pytest.fixture(autouse=True)
async def run_around_tests():
    """Executed before each test: deletes all records in the db"""
    await AvailabilitiesModel.all().delete()
    await ReservationsModel.all().delete()
    yield
