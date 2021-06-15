from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def userprofile_signal(sender, instance: UserModel, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
