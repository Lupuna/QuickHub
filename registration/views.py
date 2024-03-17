from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login

from user_project import services as up
from user_project_time import (
    services as upt_services,
    models as upt_models
    )

from . import forms as registration_forms


def sign_up(request):
    if request.method == 'POST':
        form = registration_forms.CustomUserCreationFrom(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.json_with_settings_info = registration_utils.create_base_settings_json_to_employee()
            user.save()

            up.create_category(user, title='Мои задачи')

            for status in upt_models.UserTimeCategory.Status:
                upt_services.create_TimeCategory(user, status=status)

            login(request, user)
            return redirect(reverse_lazy('team:homepage'))
    else:
        form = registration_forms.CustomUserCreationFrom()

    context = {'form': form}
    return render(request, 'registration/sign_up.html', context)