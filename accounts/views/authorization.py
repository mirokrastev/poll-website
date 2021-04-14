from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from accounts.forms import LoginForm
from django.http import Http404


class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request.user, user)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        username, password = form.cleaned_data.values()
        user = authenticate(self.request.user, **{'username': username, 'password': password})

        if not user:
            context = {'form': form, 'error': 'Incorrect credentials!'}
            return self.render_to_response(context)

        login(self.request, user)
        return redirect('home')


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'POST':
            raise Http404
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(self.request)
        return redirect('home')
