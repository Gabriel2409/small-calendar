from app.models.tortoise_models import AvailabilitiesModel, ReservationsModel
from tortoise.contrib.pydantic.creator import pydantic_model_creator

# * PAYLOADS FOR THE DB ROUTES

# * Pydantic schemas, automatically generated from tortoise models

AvailabilitiesSchema = pydantic_model_creator(AvailabilitiesModel)
ReservationsSchema = pydantic_model_creator(ReservationsModel)
