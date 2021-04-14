from django import forms
from poll.models import Question, Answer, Comment
from django.forms import modelformset_factory


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question',)


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_permitted = False

    class Meta:
        model = Answer
        fields = ('answer',)


class PollForm(forms.Form):
    answers = forms.ModelChoiceField(queryset=Answer.objects.none())
    # Give a queryset in views to answers field.


# model formset for creating multiple Answer objects (used when creating a new Poll)
answer_modelformset = modelformset_factory(model=Answer, form=AnswerForm,
                                           validate_min=True, extra=1, max_num=8)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
