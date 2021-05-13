from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from poll.api.serializers import PollSerializer
from poll.common import PollDataMixin
from poll.models import Poll, Answer, Vote


class APIPollViewer(ListModelMixin,
                    GenericAPIView
                    ):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class APIViewPoll(PollDataMixin, APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None
        self.queryset = None
        self.votes = None

    def dispatch(self, request, *args, **kwargs):
        self.object = Poll.objects.get(id=self.kwargs['poll_id'],
                                       question=self.kwargs['poll'])
        self.queryset = Answer.objects.filter(question_id=self.object.id)
        self.votes = Vote.objects.filter(answer__in=self.queryset)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        data = {'question': self.object.question,
                'answers': self.get_answer_json()}

        for key in data['answers']:
            data['answers'][key] = {'votes': data['answers'][key][0],
                                    'percents': data['answers'][key][1]}

        return Response(data=data, status=status.HTTP_200_OK)
