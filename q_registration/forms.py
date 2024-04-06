from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, SetPasswordForm, PasswordResetForm
from django.utils.translation import gettext_lazy as _
from team import models as team_models
from django import forms


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'placeholder': 'email'}),
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'placeholder': 'Пароль'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'placeholder': 'Подтвердите пароль'}),
    )


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
