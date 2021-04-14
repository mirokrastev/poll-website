from django.shortcuts import render
from django.views import View
from django.views.generic.base import ContextMixin
from poll.models import Answer, Vote, Question
from poll.forms import QuestionForm, answer_modelformset, PollForm, CommentForm
from django.http import JsonResponse, Http404
from utils.base import BaseRedirectFormView


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'home/home.html')


class PollViewer(ContextMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.polls = None

    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'GET':
            raise Http404
        self.polls = Question.objects.all()
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(self.request, 'poll/polls_viewer.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['polls'] = self.polls
        return context


class CreatePoll(ContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(self.request, 'poll/create_poll.html', context)

    def post(self, request, *args, **kwargs):
        form = QuestionForm(self.request.POST)
        formset = answer_modelformset(self.request.POST)

        if not form.is_valid() or not formset.is_valid():
            form_kwargs = {'answer_formset': formset,
                           'question_form': form}

            return self.get(self.request, **form_kwargs)

        self.form_valid(form, formset)

    def form_valid(self, form, formset):
        form = form.save(commit=False)
        formset = formset.save(commit=False)

        form.user = self.request.user
        form.save()

        for sub_form in formset:
            sub_form.question = form
        Answer.objects.bulk_create(formset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_form = kwargs.get('question_form', QuestionForm)
        answer_formset = kwargs.get('answer_formset', answer_modelformset(queryset=Answer.objects.none()))

        context.update({
            'question_form': question_form,
            'answer_formset': answer_formset,
        })

        return context


class SinglePollViewer(ContextMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = None
        self.votes = None

    def dispatch(self, request, *args, **kwargs):
        self.queryset = Answer.objects.filter(question_id=self.kwargs['poll_id'])
        self.votes = Vote.objects.filter(answer__in=self.queryset)
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('ajax', None) == 'true':
            percent_obj = {}
            for answer in self.queryset:
                votes = self.votes.filter(answer=answer)
                percent_obj[str(answer)] = (len(votes), (len(votes) * 100) / (len(self.votes) or 1))
            return JsonResponse(percent_obj)

        context = self.get_context_data()
        return render(self.request, 'poll/single-poll/view_poll.html', context)

    def post(self, request, *args, **kwargs):
        option_id = int(self.request.POST['answers'][0])
        option = self.queryset.get(id=option_id)
        Vote.objects.create(answer=option, user=self.request.user)

    def get_context_data(self, **kwargs):
        has_voted = False
        try:
            if self.request.user.is_authenticated:
                has_voted = bool(self.votes.get(user=self.request.user))
        except Vote.DoesNotExist:
            pass

        context = super().get_context_data(**kwargs)

        context.update({'poll_id': self.kwargs['poll_id'],
                        'poll': self.kwargs['poll'],
                        'has_voted': has_voted})

        if self.request.user.is_authenticated and not has_voted:
            form = PollForm()
            form.fields['answers'].queryset = self.queryset

            context.update({'form': form,
                            'comment_form': CommentForm()})

        return context


class PollComment(BaseRedirectFormView):
    form_class = CommentForm
    success_url = 'poll:poll_view'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.poll = None

    def dispatch(self, request, *args, **kwargs):
        self.poll = Question.objects.get(question_id=self.kwargs['poll_id'], question=self.kwargs['poll'])
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        form.answer = self.poll
        form.save()
        return self.redirect(redirect_kwargs={'poll': self.kwargs['poll'],
                                              'poll_id': self.kwargs['poll_id']})
