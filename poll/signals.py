from django.dispatch import receiver
from django.db.models.signals import post_save
from poll.models import Poll, UserPollTelemetry


@receiver(post_save, sender=Poll)
def telemetry_signal(sender, instance: Poll, created, **kwargs):
    if instance.telemetry and created:
        # Create Telemetry object and add Poll's owner to M2M table.
        telemetry = UserPollTelemetry.objects.create(poll=instance)
        telemetry.users.add(instance.user)
        telemetry.save()
