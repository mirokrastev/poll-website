from django.urls import path
from poll.api.views import APIPollViewer

urlpatterns = [
    path('', APIPollViewer.as_view(), name='api-poll_viewer')
]
