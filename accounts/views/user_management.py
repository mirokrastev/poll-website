from django.shortcuts import render
from django.views import View
from django.views.generic.base import ContextMixin
from poll.models import Poll
from django.http import Http404


class UserProfileView(ContextMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.polls = None

    def dispatch(self, request, *args, **kwargs):
        if self.request.method != 'GET' or self.kwargs['user'] != self.request.user.username:
            raise Http404
        self.polls = Poll.objects.filter(user=self.request.user)
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(self.request, 'accounts/user-management/user-management.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['polls'] = self.polls
        return context
