from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic.base import ContextMixin
from poll.mixins import PollObjectMixin, InitializePollMixin
from poll.models import Answer, Vote, Poll
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
        # TODO: Paginate polls
        self.polls = Poll.objects.all()
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
            # Passes the same forms to be rendered with errors
            form_kwargs = {'answer_formset': formset,
                           'question_form': form}

            return self.get(self.request, **form_kwargs)

        self.form_valid(form, formset)
        return redirect('poll:poll_viewer')

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

        # kwargs.get() is checking if there is form in kwargs. If not, instantiate new Form,
        # else render the passed form.
        question_form = kwargs.get('question_form', QuestionForm())
        answer_formset = kwargs.get('answer_formset', answer_modelformset(queryset=Answer.objects.none()))

        context.update({
            'question_form': question_form,
            'answer_formset': answer_formset,
        })

        return context


class SinglePollViewer(PollObjectMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ORM Querying
        self.object = None
        self.queryset = None
        self.votes = None
        self.user_vote = None

        # Permission checks
        self.is_trusted = False
        self.has_voted = False
        self.can_vote = False

    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'GET':
            raise Http404

        # ORM Querying
        try:
            self.object = self.get_object()

            self.queryset = Answer.objects.filter(question_id=self.object.id)
            self.votes = Vote.objects.filter(answer__in=self.queryset)

        except Poll.DoesNotExist:
            raise Http404

        # Permission checks
        self.is_trusted = self.object.user == self.request.user

        try:
            self.user_vote = self.votes.get(user=self.request.user)
            self.has_voted = bool(self.user_vote)
        except Vote.DoesNotExist:
            pass

        self.can_vote = self.request.user.is_authenticated and not self.has_voted

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = PollForm()
        form.fields['answers'].queryset = self.queryset

        context.update({'poll': self.object,
                        'answers': self.queryset,
                        'can_vote': self.can_vote,
                        'is_trusted': self.is_trusted,
                        'form': form})

        if not self.can_vote:
            form.fields['answers'].widget.attrs['disabled'] = True

        if self.has_voted:
            form.fields['answers'].initial = self.user_vote.answer.id

        return context


class PollVote(PollObjectMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None
        self.queryset = None
        self.user_vote = None
        self.has_voted = False

    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'POST':
            raise Http404
        self.object = self.get_object()
        self.queryset = Answer.objects.filter(question_id=self.object.id)
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        option_id = int(self.request.POST['answers'][0])
        option = self.queryset.get(id=option_id)
        Vote.objects.create(answer=option, user=self.request.user)
        return redirect(reverse('poll:view_poll', kwargs={'poll_id': self.object.id,
                                                          'poll': self.object}))


class PollComment(InitializePollMixin, BaseRedirectFormView):
    form_class = CommentForm
    success_url = 'poll:view_poll'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        form.answer = self.object
        form.save()
        return self.redirect(redirect_kwargs={'poll': self.kwargs['poll'],
                                              'poll_id': self.kwargs['poll_id']})


class PollDelete(InitializePollMixin, View):
    admin_only = True

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(self.request, 'poll/single-poll/delete.html', context)

    def post(self, request, *args, **kwargs):
        self.object.delete()
        return redirect('poll:poll_viewer')
