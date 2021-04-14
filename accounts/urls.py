from django.urls import path
from accounts.views.authorization import RegisterView, LoginView, LogoutView
from django.contrib.auth.decorators import login_required

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout', login_required(LogoutView.as_view()), name='logout'),
]
