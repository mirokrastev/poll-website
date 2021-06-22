from django.db import models
from django.contrib.auth import get_user_model
from poll.models.poll_models import Poll


class BasePollTelemetry(models.Model):
    """
    This Base class gives a hint that in the future
    more Telemetry classes could be implemented.
    """

    poll = models.ForeignKey(db_index=True, to=Poll, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.poll)

    class Meta:
        abstract = True


class AnonymousUserPollTelemetry(models.Model):
    """
    To "store" the anonymous users that have viewed the Poll,
    I need to store their IP Addresses. It will NEVER be displayed outside the admin panel.
    """

    anonymous_user = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.anonymous_user


class UsersPollTelemetry(BasePollTelemetry):
    users = models.ManyToManyField(db_index=True, to=get_user_model())
    anonymous_users = models.ManyToManyField(db_index=True, to=AnonymousUserPollTelemetry)

    class Meta:
        verbose_name = 'PollTelemetry'
        verbose_name_plural = 'PollTelemetry'
