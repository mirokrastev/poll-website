from django.db import models
from django.contrib.auth import get_user_model


class Poll(models.Model):
    question = models.CharField(db_index=True, max_length=50, null=False, blank=False)
    user = models.ForeignKey(db_index=True, to=get_user_model(), on_delete=models.CASCADE, null=False, blank=True)

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(db_index=True, to=Poll, on_delete=models.CASCADE, null=False, blank=True)
    answer = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.answer


class Vote(models.Model):
    answer = models.ForeignKey(db_index=True, to=Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    question = models.ForeignKey(to=Poll, on_delete=models.CASCADE, null=False, blank=True)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, null=False, blank=True)
    comment = models.TextField(max_length=250, null=False, blank=True)
