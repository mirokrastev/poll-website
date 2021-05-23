from django.contrib import admin
from poll.models.poll_models import Poll, Answer, Vote, Comment
from poll.models import UserPollTelemetry


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    max_num = 8


class UserPollTelemetryInline(admin.TabularInline):
    model = UserPollTelemetry
    extra = 1
    max_num = 1
    can_delete = False


class PollAdminPanel(admin.ModelAdmin):
    exclude = ('telemetry',)
    inlines = (AnswerInline, UserPollTelemetryInline)


admin.site.register(Poll, PollAdminPanel)
admin.site.register(Vote)
admin.site.register(Comment)
