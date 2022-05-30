from app.config import Settings, get_settings
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/")
def hello(settings: Settings = Depends(get_settings)):
    """Hello world route to make sure the app is working correctly"""
    return {"Hello": "World", "env": settings.env}
