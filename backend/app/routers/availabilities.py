from datetime import timedelta

from app.models.pydantic_schemas import AvailabilitiesPayload, AvailabilitiesSchema
from app.models.tortoise_models import AvailabilitiesModel
from app.utils.datetime_operations import get_previous_time_slot
from fastapi import HTTPException
from fastapi_crudrouter import TortoiseCRUDRouter as CRUDRouter
from tortoise.expressions import Q

# generates get all, get one and delete one route
router = CRUDRouter(
    schema=AvailabilitiesSchema,
    db_model=AvailabilitiesModel,
    # create_schema=AvailabilitiesPayload,
    create_route=False,
    delete_all_route=False,
    update_route=False,
    prefix="/api/availabilitieslabilities",
)


@router.post("")
async def post_availability(payload: AvailabilitiesPayload):
    """Posts an availability to the db.

    Note that this route is not generated automatically by the crudrouter
    because we need to add custom logic: we can only create an availability
    if it does not overlap with existing availabilities, end should be after
    start but on the same day. And finally, end and start are rounded back to the
    previous 5 minute time slot to avoid having strange availabilities

    Args:
        payload (AvailabilitiesPayload): the body of the post request
    """

    payload.start = get_previous_time_slot(payload.start)
    payload.end = get_previous_time_slot(payload.end)

    if payload.start >= payload.end:
        raise HTTPException(
            status_code=400, detail="end should be at least 5 minutes after start"
        )
    if payload.end - payload.start >= timedelta(hours=12):
        raise HTTPException(
            status_code=400, detail="Availabilities can not last more than 12 hours"
        )

    # checks that no already existing availabilities conflict with current payload
    conflicting_records = await AvailabilitiesModel.filter(
        Q(start__lte=payload.start, end__gt=payload.start)
        | Q(start__lt=payload.end, end__gte=payload.end)
        | Q(start__gte=payload.start, end__lte=payload.end)
    )

    if conflicting_records:
        raise HTTPException(status_code=409, detail="Availabilities cannot overlap")
    record = AvailabilitiesModel(**payload.dict())

    await record.save()
    return record
