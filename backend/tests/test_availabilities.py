"""Tests for the availabilities crud operations. Note that the get, get all and
delete are generated by CRUDRouter so there is no need to test them."""
from datetime import datetime, timedelta, timezone

from pydantic.datetime_parse import parse_datetime


def test_post_availability(test_app):
    """Test the post route, first by checking that an object is correctly added, then
    by adding invalid and conflicting cases and checking they are not added
    """
    response = test_app.post(
        "/api/availabilitieslabilities",
        json={"start": "2022-05-31T06:57", "end": "2022-05-31T07:57"},
    )
    assert response.status_code == 200
    assert "id" in response.json()

    # check created_at is correctly added
    created_at = parse_datetime(response.json()["created_at"])
    assert (datetime.utcnow().replace(tzinfo=timezone.utc) - created_at) < timedelta(
        seconds=5
    )
    # check time was rounded to last 5 min slot
    assert response.json()["start"] == "2022-05-31T06:55:00+00:00"
    assert response.json()["end"] == "2022-05-31T07:55:00+00:00"

    # bad requests
    for obj in [
        # end is equal to start
        {"start": "2022-05-31T04:40", "end": "2022-05-31T04:40"},
        # end is before start
        {"start": "2022-05-31T04:40", "end": "2022-05-31T04:30"},
        {"start": "2022-05-31T04:40", "end": "2022-05-30T04:50"},
        # end is too far in the future
        {"start": "2022-05-31T04:40", "end": "2023-05-31T04:50"},
    ]:

        response = test_app.post("/api/availabilitieslabilities", json=obj)
        assert response.status_code == 400

    # conflicts:
    for obj in [
        # equal
        {"start": "2022-05-31T06:55", "end": "2022-05-31T07:55"},
        # contained in
        {"start": "2022-05-31T06:55", "end": "2022-05-31T07:00"},
        {"start": "2022-05-31T07:00", "end": "2022-05-31T07:55"},
        {"start": "2022-05-31T07:00", "end": "2022-05-31T07:05"},
        # start in
        {"start": "2022-05-31T07:00", "end": "2022-05-31T08:05"},
        # end in
        {"start": "2022-05-31T06:00", "end": "2022-05-31T07:00"},
        # contains
        {"start": "2022-05-31T05:00", "end": "2022-05-31T09:00"},
    ]:
        response = test_app.post("/api/availabilitieslabilities", json=obj)
        assert response.status_code == 409

    # assert it works if just after or just before
    for obj in [
        {"start": "2022-05-31T05:55", "end": "2022-05-31T06:55"},
        {"start": "2022-05-31T07:55", "end": "2022-05-31T08:55"},
    ]:
        response = test_app.post("/api/availabilitieslabilities", json=obj)
        assert response.status_code == 200
