from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from poll.api.serializers import PollSerializer
from poll.models import Poll, Answer


class APIPollViewer(ListModelMixin,
                    GenericAPIView
                    ):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class APIViewPoll(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None
        self.answers = None

    def dispatch(self, request, *args, **kwargs):
        self.object = Poll.objects.get(id=self.kwargs['poll_id'],
                                       question=self.kwargs['poll'])
        self.answers = Answer.objects.filter(question=self.object)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        data = {'question': self.object.question,
                'answers': {
                    num: str(value)
                    for num, value in enumerate(self.answers, start=1)
                }}
        return Response(data=data, status=status.HTTP_200_OK)
