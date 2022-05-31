import math
from datetime import datetime, timezone


def get_previous_time_slot(
    current_time: datetime, slot_duration_in_minutes: int = 5
) -> datetime:
    """Gets the previous time slot.
    Note: also sets the timezone to utc if not present

    This function truncates the timeslot to the previous time slot so that its
    minutes become a duration of slot_duration_in_minutes.

    Args:
        current_time (datetime): the current time
        slot_duration_in_minutes (int) the closest slot to fall back to. Defaults to 5
    Returns
        datetime : the rounded datetime
    """
    base = 5
    tz = timezone.utc if not current_time.tzinfo else current_time.tzinfo

    rounded_datetime = current_time.replace(
        microsecond=0,
        second=0,
        minute=base * math.floor(current_time.minute / base),
        tzinfo=tz,
    )

    return rounded_datetime
