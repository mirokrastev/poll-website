from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import ContextMixin
from poll.models.poll_models import Poll
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


class DeleteUserView(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'accounts/delete.html')

    def post(self, request, *args, **kwargs):
        self.request.user.delete()
        return redirect('home')


class SettingsView(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'accounts/user-management/settings.html')
