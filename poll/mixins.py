from django.views.generic.detail import SingleObjectMixin
from poll.common import PollTrackUsersMixin
from django.http import Http404
from poll.models.poll_models import Poll


class PollObjectMixin(SingleObjectMixin):
    model = Poll

    pk_url_kwarg = 'poll_id'

    slug_field = 'slug'
    slug_url_kwarg = 'poll'
    query_pk_and_slug = True

    context_object_name = 'poll'


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
