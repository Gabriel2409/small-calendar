import pytest
from app.application_factory import create_app
from app.config import Settings, get_settings
from fastapi.testclient import TestClient


def get_settings_override() -> Settings:
    """Overrides the settings for testing

    Returns:
        Settings: fastapi test settings
    """
    return Settings(env="testing")


@pytest.fixture(scope="module")
def test_app():
    """test client"""
    # set up
    app = create_app()
    app.dependency_overrides[get_settings] = get_settings_override

    # testing
    with TestClient(app) as test_client:
        yield test_client

    # tear down
