from datetime import timedelta

from app.models.pydantic_schemas import ReservationsPayload, ReservationsSchema
from app.models.tortoise_models import AvailabilitiesModel, ReservationsModel
from app.utils.datetime_operations import get_previous_time_slot
from app.utils.iterator import pairwise
from app.utils.string_operations import obfuscate_string
from fastapi import APIRouter, HTTPException
from tortoise.expressions import Q

router = APIRouter(prefix="/api/reservations")


@router.post("")
async def post_reservation(payload: ReservationsPayload):
    """Posts a reservation to the db.

    We can only create a reservation if it does not overlap with existing reservations =
    same logic as availabilities (we could make a function to avoid repeating the code).
    Moreover, we need to make sure that the reservations do not overlap with unavailable
    slots.

    NOTE: combining non overlapping reservations and non overlapping unavailable times
    are enough to make sure that we can not set up a reservation at an unwanted time.
    Therefore, there is no need to modify the availabilities table when creating a
    reservation.


    Args:
        payload (ReservationsPayload): the body of the post request
    """

    # same logic as availabilities
    payload.start = get_previous_time_slot(payload.start)
    payload.end = get_previous_time_slot(payload.end)

    if payload.start >= payload.end:
        raise HTTPException(
            status_code=400, detail="end should be at least 5 minutes after start"
        )
    if payload.end - payload.start >= timedelta(hours=12):
        raise HTTPException(
            status_code=400, detail="Reservations can not last more than 12 hours"
        )

    # checks that no already existing availabilities conflict with current payload
    conflicting_records = await ReservationsModel.filter(
        Q(start__lte=payload.start, end__gt=payload.start)
        | Q(start__lt=payload.end, end__gte=payload.end)
        | Q(start__gte=payload.start, end__lte=payload.end)
    )

    if conflicting_records:
        raise HTTPException(status_code=409, detail="Reservations cannot overlap")

    # also check that reservation does not overlap with unavailable slots
    corresponding_availabilities = await AvailabilitiesModel.filter(
        Q(start__lte=payload.start, end__gt=payload.start)
        | Q(start__lt=payload.end, end__gte=payload.end)
        | Q(start__gte=payload.start, end__lte=payload.end)
    ).order_by("start")

    if (
        not corresponding_availabilities
        or corresponding_availabilities[0].start > payload.start
        or corresponding_availabilities[-1].end < payload.end
    ):
        raise HTTPException(
            status_code=400,
            detail="Reservations can not be made at unavailable slots",
        )

    for cur_av, next_av in pairwise(corresponding_availabilities):
        if next_av is None:
            break
        if cur_av.end < next_av.start:
            raise HTTPException(
                status_code=400,
                detail="Reservations can not be made at unavailable slots",
            )
    record = ReservationsModel(**payload.dict())
    await record.save()
    return record


@router.get("")
async def get_all_reservations():
    """Gets all the current reservations. Email is obfuscated so that end user can
    not delete it easily.
    """
    records = await ReservationsModel.all()
    obfuscated_records = []
    for record in records:
        new_rec = await ReservationsSchema.from_tortoise_orm(record)
        new_rec.email = obfuscate_string(record.email)
        obfuscated_records.append(new_rec)
    return obfuscated_records


@router.delete("/{id}/{email}")
async def delete_reservation(id: int, email: str):
    """
    Deletes a reservation. The user must pass the correct email to delete it.

    Note: This does not handle emails with very strange characters.

    Args:
        id (int): the id of the reservation
        email (str): the email
    """

    # will throw a 404 if record does not exist
    record = await ReservationsModel.get(id=id, email=email)
    await record.delete()
    return record
