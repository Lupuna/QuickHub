from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from team import models as team_models
from django import forms


class CustomUserCreationFrom(UserCreationForm):

    class Meta:
        model = team_models.Employee
        fields = ('name', 'username', 'email', 'password1', 'password2')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'username': forms.TextInput(attrs={'placeholder': 'Логин'}),
            'email': forms.TextInput(attrs={'placeholder': 'Почта'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationFrom, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Пароль'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'})


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
