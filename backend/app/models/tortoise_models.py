from tortoise import fields, models


class TimestampMixin:
    """Timestamp fields"""

    # automatically added on record creation
    created_at = fields.DatetimeField(auto_now_add=True)
    # automatically added on record modification
    updated_at = fields.DatetimeField(auto_now=True)


class AbstractBaseModel(models.Model):
    """Abstract base model for clauses."""

    id = fields.IntField(pk=True)

    class Meta:
        """Abstract Base model does not appear in db"""

        abstract = True


class AvailabilitiesModel(TimestampMixin, AbstractBaseModel):
    """Models for storing the availabilites.

    Fields:
        start :  the starting datetime of the availability
        end : the ending datetime of the availability
    """

    start = fields.DatetimeField()
    end = fields.DatetimeField()

    class Meta:
        """table name"""

        table = "availabilities"


class ReservationsModel(TimestampMixin, AbstractBaseModel):
    """Models for storing the reservations.
    Fields:
        start :  the starting datetime of the reservation
        end :the ending datetime of the reservation
        title : the title of the reservation
        email : the email of the person booking a reservation
    """

    start = fields.DatetimeField()
    end = fields.DatetimeField()
    title = fields.CharField(max_length=255, unique=False, null=False)
    email = fields.CharField(max_length=255, unique=False, null=False)
    # Note: email validity must be enforced in backend before storing in db

    class Meta:
        """table name"""

        table = "reservations"
