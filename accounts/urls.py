from django.urls import path
from accounts.views.authorization import RegisterView, LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from accounts.views.user_management import UserProfileView, DeleteUserHybridView, ChangePasswordHybridView, \
    ChangeTelemetryHybridView

app_name = 'accounts'


urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout', login_required(LogoutView.as_view()), name='logout'),

    # Account Management
    path('', login_required(UserProfileView.as_view()), name='my_profile'),
    path('password/change', login_required(ChangePasswordHybridView.as_view()), name='change_password'),
    path('telemetry', login_required(ChangeTelemetryHybridView.as_view()), name='change_telemetry'),
    path('delete', login_required(DeleteUserHybridView.as_view()), name='delete_user'),
]
