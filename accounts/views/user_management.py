from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from utils.mixins import PaginateObjectMixin
from django.contrib.auth.forms import PasswordChangeForm
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

        context = {
            'polls': polls,
            'paginator': paginator,
            'is_paginated': polls.has_other_pages()
        }

        context = self.get_context_data(**context)
        return render(self.request, 'accounts/user-management/user-management.html', context)


class ChangePasswordView(FormView):
    # This is a Django form for changing password. It it fairly easy to do it manually,
    # But I prefer to use the built-in forms.
    form_class = PasswordChangeForm
    template_name = 'accounts/change-password.html'

    def form_valid(self, form):
        form.save()
        return redirect('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DeleteUserView(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'accounts/delete.html')

    def post(self, request, *args, **kwargs):
        self.request.user.delete()
        return redirect('home')
