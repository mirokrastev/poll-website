from django.contrib import admin
from poll.models.poll_models import Poll, Answer, Vote, Comment
from poll.models import UserPollTelemetry

admin.site.register(Poll)
admin.site.register(Answer)
admin.site.register(Vote)
admin.site.register(Comment)
admin.site.register(UserPollTelemetry)
