from django.urls import path
from accounts.views.authorization import RegisterView, LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from accounts.views.user_management import UserProfileView, SettingsView, DeleteUserView, ChangePasswordView

app_name = 'accounts'


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout', login_required(LogoutView.as_view()), name='logout'),
    path('delete', login_required(DeleteUserView.as_view()), name='delete_user'),

    path('settings', login_required(SettingsView.as_view()), name='settings'),
    path('password/change', login_required(ChangePasswordView.as_view()), name='change_password'),
    # TODO: Refactor.
    path('<str:user>', login_required(UserProfileView.as_view()), name='my_polls'),
]
