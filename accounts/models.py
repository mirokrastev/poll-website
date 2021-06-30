from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserProfile(models.Model):
    """
    This model is extending the User model indirectly, rather than changing
    the AUTH_USER_MODEL by inheriting from AbstractUser
    """
    user = models.OneToOneField(to=UserModel, on_delete=models.CASCADE, related_name='user_profile')
    telemetry = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)
