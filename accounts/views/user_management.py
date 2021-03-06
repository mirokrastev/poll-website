from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView
from accounts.forms import TelemetryForm
from utils.mixins import PaginateObjectMixin
from django.views.generic.base import ContextMixin
from poll.models.poll_models import Poll
from django.http import Http404


class UserProfileView(PaginateObjectMixin, ContextMixin, View):
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'GET':
            raise Http404
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        page = self.request.GET.get('page', 1)
        paginator, polls = self.paginate(Poll.objects.filter(user=self.request.user), page)

        context_kwargs = {
            'polls': polls,
            'paginator': paginator,
            'is_paginated': polls.has_other_pages()
        }

        context = self.get_context_data(**context_kwargs)

        api_call = self.request.GET.get('api', None) == 'true'

        if api_call:
            return render(self.request, 'accounts/user-management/spa-components/home-component.html', context)
        return render(self.request, 'accounts/user-management/user-management.html', context)


class ChangePasswordHybridView(FormView):
    form_class = PasswordChangeForm
    template_name = 'accounts/user-management/spa-components/change-password-component.html'

    def form_valid(self, form):
        form.save()
        return redirect('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'action_url': reverse('accounts:change_password'),
                        'auth_header': 'CHANGE'})
        return context


class DeleteUserHybridView(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'accounts/user-management/spa-components/delete-component.html')

    def post(self, request, *args, **kwargs):
        self.request.user.delete()
        return redirect('home')


class ChangeTelemetryHybridView(ContextMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_profile = None

    def dispatch(self, request, *args, **kwargs):
        self.user_profile = self.request.user.user_profile
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context_kwargs = {
            'form': TelemetryForm(instance=self.user_profile)
        }

        context = self.get_context_data(**context_kwargs)
        return render(self.request, 'accounts/user-management/spa-components/'
                                    'change-telemetry-component.html', context)

    def post(self, request, *args, **kwargs):
        self.user_profile.telemetry = not self.user_profile.telemetry
        self.user_profile.save()
        return redirect('accounts:my_profile')
