from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from team import models as team_models
from django import forms


class CustomUserCreationFrom(UserCreationForm):
    class Meta:
        model = team_models.Employee
        fields = ('name', 'username', 'email', 'password1', 'password2')


class AuthenticationFormCustom(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        "autofocus": True,
        'placeholder': 'Логин',
    }))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            'placeholder': 'Пароль',
        }),
    )

    remember_me = forms.BooleanField(initial=True, required=False)
