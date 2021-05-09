from django.urls import path
from poll.api.views import APIPollViewer, APIViewPoll

urlpatterns = [
    path('', APIPollViewer.as_view(), name='api-poll_viewer'),
    path('<int:poll_id>/<str:poll>', APIViewPoll.as_view(), name='api-view_poll'),
]
