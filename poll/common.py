from poll.models import UsersPollTelemetry, AnonymousUserPollTelemetry


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
        """
        Ignore everything related to Telemetry if "telemetry" field is False.
        """
        if not self.object.telemetry or not self.request.user.user_profile.telemetry:
            return super().dispatch(self.request, *args, **kwargs)

        telemetry = UsersPollTelemetry.objects.get(poll=self.object)

        if self.request.user.is_authenticated:
            self._authenticated_telemetry(telemetry)
        else:
            self._anonymous_telemetry(telemetry)

        return super().dispatch(self.request, *args, **kwargs)

    def _authenticated_telemetry(self, telemetry):
        telemetry.users.add(self.request.user)
        telemetry.save()

    def _anonymous_telemetry(self, telemetry):
        client_ip = self.request.META['REMOTE_ADDR']
        address_object = AnonymousUserPollTelemetry.objects.get_or_create(
            anonymous_user=client_ip
        )[0]

        telemetry.anonymous_users.add(address_object)
        telemetry.save()
