from django.dispatch import receiver
from django.db.models.signals import post_save
from poll.models import Poll, UsersPollTelemetry


@receiver(post_save, sender=Poll)
def telemetry_signal(sender, instance: Poll, created, **kwargs):
    if instance.telemetry and created:
        # Create Telemetry object
        telemetry = UsersPollTelemetry.objects.create(poll=instance)
