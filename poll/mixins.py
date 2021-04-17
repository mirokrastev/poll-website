from django.views.generic.detail import SingleObjectMixin
from poll.models import Poll
from django.http import Http404


class PollObjectMixin(SingleObjectMixin):
    model = Poll

    pk_url_kwarg = 'poll_id'

    slug_url_kwarg = 'poll'
    slug_field = 'question'

    query_pk_and_slug = True

    context_object_name = 'poll'


class InitializePollMixin(PollObjectMixin):
    admin_only = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.admin_only and self.object.user != self.request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
