from django import forms
from django.contrib.auth.password_validation import MinimumLengthValidator


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=25, required=True,
                               error_messages={
                                   'min_length': 'Your username must be at least 4 characters long.'
                               })
    password = forms.CharField(widget=forms.PasswordInput(), required=True, validators=[MinimumLengthValidator])
