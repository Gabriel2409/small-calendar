from datetime import datetime

from app.models.tortoise_models import AvailabilitiesModel, ReservationsModel
from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic.creator import pydantic_model_creator

# note regarding pydantic datetime.
# if you don't pass a timezone, it will default to UTC.
# to pass CET timezone, just pass +02:00 at the end of the time

# * Payloads for the db routes


class AvailabilitiesPayload(BaseModel):
    """Payload for post / put request"""

    start: datetime
    end: datetime


class ReservationsPayload(BaseModel):
    """Payload for post / put request"""

    start: datetime
    end: datetime
    title: str
    email: EmailStr


# * Pydantic schemas, automatically generated from tortoise models

AvailabilitiesSchema = pydantic_model_creator(AvailabilitiesModel)
ReservationsSchema = pydantic_model_creator(ReservationsModel)
