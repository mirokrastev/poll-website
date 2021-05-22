from poll.models import UserPollTelemetry


class PollDataMixin:
    """
    Mixin to share logic for Poll Data (percents, likes, etc)
    It should be inherited by View with queryset and votes attributes
    """

    def get_answer_json(self):
        answers_dict = {}
        for answer in self.queryset:
            votes = self.votes.filter(answer=answer)
            answers_dict[str(answer)] = (len(votes), (len(votes) * 100) / (len(self.votes) or 1))
        return answers_dict


class PollTrackUsersMixin:
    """
    To use this Mixin, you need to provide self.object that is an instance of Poll model
    """

    def dispatch(self, request, *args, **kwargs):
        if self.object.telemetry and self.request.user.is_authenticated:
            telemetry = UserPollTelemetry.objects.get(poll=self.object)
            telemetry.users.add(self.request.user)
            telemetry.save()

        return super().dispatch(self.request, *args, **kwargs)
