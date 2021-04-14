from django.urls import path
from poll.views import PollViewer, CreatePoll, PollComment, SinglePollViewer
from django.contrib.auth.decorators import login_required

app_name = 'poll'

urlpatterns = [
    path('', PollViewer.as_view(), name='poll_viewer'),
    path('create', login_required(CreatePoll.as_view()), name='create_poll'),
    path('<int:poll_id>/<str:poll>', SinglePollViewer.as_view(), name='view_poll'),
    path('<int:poll_id>/<str:poll>/comment', login_required(PollComment.as_view()), name='comment_poll'),
]
