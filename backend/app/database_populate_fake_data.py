"""Script to launch after generating the db to populate it with fake data.
Allows to test the app rapidly"""


import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from models.tortoise_models import AvailabilitiesModel, ReservationsModel
from tortoise import Tortoise, run_async
from utils.datetime_operations import get_previous_time_slot

load_dotenv()


async def populate_db():
    """Adds fake data to the db to allow to use the app easily.
    NOTE: schemas must be generated prior to calling this function
    """
    await Tortoise.init(
        db_url=os.getenv("DATABASE_URL", ""),
        modules={"models": ["models.tortoise_models"]},
    )
    local_timezone = datetime.now(timezone.utc).astimezone().tzinfo
    current_datetime = datetime.now(tz=local_timezone)
    corresponding_monday = current_datetime - timedelta(days=current_datetime.weekday())

    # populates current week + monday and tuesday of next week.
    # 4 available slots of 2 hours each day
    for daynb in list(range(5)) + [7, 8]:
        for hour in [8, 10, 14, 16]:
            start_time = get_previous_time_slot(
                (corresponding_monday + timedelta(days=daynb)).replace(
                    hour=hour, minute=0
                )
            )
            end_time = start_time.replace(hour=hour + 2)

            availability = AvailabilitiesModel(start=start_time, end=end_time)
            await availability.save()

        # we also add a unique reservation overlapping between 9h and 11h
        start_time = get_previous_time_slot(
            (corresponding_monday + timedelta(days=daynb)).replace(hour=9, minute=0)
        )
        end_time = start_time.replace(hour=11)
        reservation = ReservationsModel(
            start=start_time,
            end=end_time,
            title="Fake Reservation",
            email="delete@me.com",
        )
        await reservation.save()


if __name__ == "__main__":
    run_async(populate_db())
