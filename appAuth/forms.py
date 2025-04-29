from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    username = forms.CharField(label="Username: ", max_length=100)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    passwordCheck = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        User = get_user_model()
        users = User.objects.all()

        clean_username = self.cleaned_data['username']

        # Check if a date is not in the past.
        for items in users:
            if clean_username == items.username:
                raise ValidationError(('Username exists'))

        if cleaned_data['password'] != cleaned_data['passwordCheck']:
            raise ValidationError(('Password does not match'))
        return cleaned_data
        # Remember to always return the cleaned data.
        return cleaned_data



class LoginForm(forms.Form):
    username = forms.CharField(label="Username: ", max_length=100)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)