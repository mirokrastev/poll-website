from django import forms
from django.forms import modelformset_factory
from poll.models.poll_models import Poll, Answer, Comment


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('name', 'telemetry')


class AnswerForm(forms.ModelForm):
    """
    Base Form to be used in formset.
    It can be used alone, but for more dynamic content, use it with formset.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_permitted = False

    class Meta:
        model = Answer
        fields = ('answer',)


# model formset for creating multiple Answer objects (used when creating a new Poll)
answer_modelformset = modelformset_factory(model=Answer, form=AnswerForm,
                                           validate_min=True, extra=1, max_num=8)


class VoteForm(forms.Form):
    answers = forms.ModelChoiceField(queryset=Answer.objects.none(),
                                     widget=forms.RadioSelect())
    # Give a queryset in views to answers field


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({
            'class': 'form-control',
            'rows': '3'
        })

    class Meta:
        model = Comment
        fields = ('comment',)
