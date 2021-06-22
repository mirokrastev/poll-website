from django.views.generic.detail import SingleObjectMixin
from poll.common import PollTrackUsersMixin
from django.http import Http404
from poll.models.poll_models import Poll
from urllib.parse import quote, unquote


class PollObjectMixin(SingleObjectMixin):
    model = Poll

    pk_url_kwarg = 'poll_id'

    slug_field = 'str'
    slug_url_kwarg = 'poll'

    context_object_name = 'poll'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        encoded_url = self.kwargs[self.slug_url_kwarg]
        decoded_url = unquote(encoded_url)

        if not obj.name == decoded_url:
            raise Http404
        return obj


class InitializePollMixin(PollObjectMixin, PollTrackUsersMixin):
    owner_only = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        """
        The .dispatch() method MRO is like this:
            Initialise the object (Poll model instance)
                -> Check if object.telemetry is True.
                    -> Continue down the MRO chain (most likely another Mixin that is initializing something
                       or View base .dispatch() method.
        """

        self.object = self.get_object()
        if self.owner_only and self.object.user != self.request.user:
            raise Http404

        return super().dispatch(request, *args, **kwargs)
