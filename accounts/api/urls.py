from django.urls import path
from accounts.api.views import LoginAPIView, RegisterAPIView

app_name = 'api-accounts'

urlpatterns = [
    path('auth-token', LoginAPIView.as_view(), name='api-auth-token'),
    path('register', RegisterAPIView.as_view(), name='api-register')
]
