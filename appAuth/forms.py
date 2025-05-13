from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from userProfile.models import USER_TYPE_CHOICES

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username',
            'class': 'input-field'
        })
    )
    password = forms.CharField(
        max_length=32,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'class': 'input-field'
        })
    )
    passwordCheck = forms.CharField(
        max_length=32,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'class': 'input-field'
        })
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'input-field'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        passwordCheck = cleaned_data.get('passwordCheck')

        if password != passwordCheck:
            self.add_error('passwordCheck', "Passwords do not match.")
        
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'class': 'input-field'
        })
    )
    password = forms.CharField(
        label="Password",
        max_length=32,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'input-field'
        })
    )
