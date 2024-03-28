from django.contrib.auth.forms import UserCreationForm
from team import models as team_models


class CustomUserCreationFrom(UserCreationForm):
    class Meta:
        model = team_models.Employee
        fields = ('name', 'username', 'email', 'password1', 'password2')