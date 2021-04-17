from django.urls import path
from accounts.views.authorization import RegisterView, LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from accounts.views.user_management import UserProfileView

app_name = 'accounts'


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout', login_required(LogoutView.as_view()), name='logout'),

    path('<str:user>', login_required(UserProfileView.as_view()), name='my_polls'),
]
