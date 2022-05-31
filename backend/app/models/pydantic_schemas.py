from datetime import datetime

from app.models.tortoise_models import AvailabilitiesModel, ReservationsModel
from pydantic import BaseModel
from tortoise.contrib.pydantic.creator import pydantic_model_creator


# * PAYLOADS FOR THE DB ROUTES
class AvailabilitiesPayload(BaseModel):
    """Payload for post / put request"""

    start: datetime
    end: datetime


# * Pydantic schemas, automatically generated from tortoise models

AvailabilitiesSchema = pydantic_model_creator(AvailabilitiesModel)
ReservationsSchema = pydantic_model_creator(ReservationsModel)
