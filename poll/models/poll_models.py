from django.db import models
from django.contrib.auth import get_user_model
from utils.managers import GenericManager

UserModel = get_user_model()


class Poll(models.Model):
    name = models.CharField(db_index=True, max_length=50, null=False, blank=False)
    telemetry = models.BooleanField(default=True)
    user = models.ForeignKey(db_index=True, to=UserModel, on_delete=models.CASCADE, null=False, blank=True)

    def __str__(self):
        return self.name


class Answer(models.Model):
    poll = models.ForeignKey(db_index=True, to=Poll, on_delete=models.CASCADE, null=False, blank=True)
    answer = models.CharField(max_length=50, null=False, blank=False)

    objects = GenericManager()

    def __str__(self):
        return self.answer


class Vote(models.Model):
    answer = models.ForeignKey(db_index=True, to=Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(to=UserModel, on_delete=models.SET_NULL, null=True, blank=True)

    objects = GenericManager()

    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    poll = models.ForeignKey(to=Poll, on_delete=models.CASCADE, null=False, blank=True)
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, null=False, blank=True)
    comment = models.TextField(max_length=250, null=False, blank=True)

    def __str__(self):
        return f'{self.user}: {self.comment}'
