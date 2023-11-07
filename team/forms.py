from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationFrom(UserCreationForm):

    class Meta:
        model = models.Employee
        fields = ('username', 'name', 'email', 'password')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = models.Employee
        fields = ('username', 'name', 'email', 'password')
