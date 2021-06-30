from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import DeleteView
from poll.common import PollDataMixin, PollTrackUsersMixin
from poll.mixins import PollObjectMixin, InitializePollMixin
from utils.mixins import PaginateObjectMixin
from poll.forms import PollForm, answer_modelformset, CommentForm, VoteForm
from django.http import JsonResponse, Http404
from poll.models import UsersPollTelemetry
from poll.models.poll_models import Poll, Answer, Vote, Comment
from utils.base import BaseRedirectFormView


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'home/home.html')


class PollViewer(ListView):
    paginate_by = 10
    model = Poll
    template_name = 'poll/poll-viewer-page/polls-viewer.html'
    context_object_name = 'polls'


class CreatePoll(ContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(self.request, 'poll/create-poll.html', context)

    def post(self, request, *args, **kwargs):
        form = PollForm(self.request.POST)
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
            sub_form.poll = form
        Answer.objects.bulk_create(formset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # kwargs.get() is checking if there is form in kwargs. If not, instantiate new Form,
        # else render the passed form.
        question_form = kwargs.get('question_form', PollForm())
        answer_formset = kwargs.get('answer_formset', answer_modelformset(queryset=Answer.objects.none()))

        context.update({
            'question_form': question_form,
            'answer_formset': answer_formset,
        })

        return context


class SinglePollViewer(PollObjectMixin, PollTrackUsersMixin, PollDataMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ORM Querying
        self.object = None
        self.queryset = None
        self.votes = None
        self.comments = None
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
            self.queryset = Answer.objects.filter(poll=self.object)
            self.votes = Vote.objects.filter(answer__in=self.queryset)
        except Poll.DoesNotExist:
            raise Http404

        self.comments = Comment.objects.filter(poll=self.object)

        # Permission checks
        if self.request.user.is_authenticated:
            self.is_trusted = self.object.user == self.request.user
            self.user_vote = Vote.objects.get_or_none(answer__in=self.queryset,
                                                      user=self.request.user)
            self.has_voted = bool(self.user_vote)
            self.can_vote = self.request.user.is_authenticated and not self.has_voted

        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('ajax', None) == 'true':
            percent_obj = self.get_answer_json()
            return JsonResponse(percent_obj)

        context = self.get_context_data()
        return render(self.request, 'poll/single-poll-page/view-poll.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = VoteForm()
        form.fields['answers'].queryset = self.queryset

        context.update({'poll': self.object,
                        'answers': self.queryset,
                        'comments': self.comments,
                        'can_vote': self.can_vote,
                        'is_trusted': self.is_trusted,
                        'form': form})

        if not self.can_vote:
            form.fields['answers'].widget.attrs['disabled'] = True

        if self.has_voted:
            form.fields['answers'].initial = self.user_vote.answer.id

        if self.request.user.is_authenticated:
            context.update({'comment_form': CommentForm()})

        return context


class PollVote(PollObjectMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None
        self.queryset = None
        self.user_vote = None

    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'POST':
            raise Http404
        self.object = self.get_object()
        print(self.object)
        self.queryset = Answer.objects.filter(poll=self.object)
        self.user_vote = Vote.objects.get_or_none(answer__in=self.queryset,
                                                  user=self.request.user)

        if self.user_vote:
            raise Http404

        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        option_id = int(self.request.POST['answers'])
        option = self.queryset.get(id=option_id)
        Vote.objects.create(answer=option, user=self.request.user)
        return redirect(reverse('poll:view_poll', kwargs={'poll_id': self.object.id,
                                                          'poll': self.object.slug}))


class PollComment(InitializePollMixin, BaseRedirectFormView):
    form_class = CommentForm
    success_url = 'poll:view_poll'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise Http404
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        form.poll = self.object
        form.save()
        return redirect(reverse('poll:view_poll', kwargs={'poll_id': self.object.id,
                                                          'poll': self.object.slug}))


class PollDelete(InitializePollMixin, DeleteView):
    owner_only = True
    success_url = reverse_lazy('poll:poll_viewer')
    template_name = 'poll/single-poll-page/delete.html'


class PollTelemetry(InitializePollMixin, PaginateObjectMixin, View):
    owner_only = True

    def dispatch(self, request, *args, **kwargs):
        if not self.request.method == 'GET':
            raise Http404
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        telemetry_object = UsersPollTelemetry.objects.get(poll=self.object)

        users_queryset = telemetry_object.users.all()
        users_count = len(users_queryset)
        anonymous_users_count = telemetry_object.anonymous_users.count()

        page = self.request.GET.get('page', 1)
        paginator, paginated_users_queryset = self.paginate(users_queryset, page)

        context_kwargs = {
            'poll': self.object,
            'paginator': paginator,

            'total_users_count': users_count + anonymous_users_count,
            'anonymous_users_count': anonymous_users_count,
            'users_count': users_count,

            'users': paginated_users_queryset,
            'is_paginated': paginated_users_queryset.has_other_pages()
        }

        context = self.get_context_data(**context_kwargs)
        return render(self.request, 'poll/single-poll-page/poll-telemetry.html', context)
