from django.db import models
from django.contrib.auth import get_user_model
from poll.models.poll_models import Poll


class BasePollTelemetry(models.Model):
    """
    This Base class gives a hint that in the future
    more Telemetry classes could be implemented.
    """

    poll = models.ForeignKey(db_index=True, to=Poll, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class UserPollTelemetry(BasePollTelemetry):
    users = models.ManyToManyField(db_index=True, to=get_user_model())

    def __str__(self):
        return str(self.poll)
