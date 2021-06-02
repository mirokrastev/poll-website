from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=25, required=True,
                               error_messages={
                                   'min_length': 'Your username must be at least 4 characters long.'
                               })
    password = forms.CharField(widget=forms.PasswordInput(), min_length=8, required=True,
                               error_messages={
                                   'min_length': 'Your password must be at least 8 characters long.'
                               })
