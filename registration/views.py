from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from user_project import models as user_project_models
from . import forms as registration_forms


def sign_up(request):
    if request.method == 'POST':
        form = registration_forms.CustomUserCreationFrom(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.json_with_settings_info = registration_utils.create_base_settings_json_to_employee()
            user.save()

            user_project_models.Category.objects.create(title='Мои задачи', employee_id=user)
            login(request, user)
            return redirect(reverse_lazy('team:homepage'))
    else:
        form = registration_forms.CustomUserCreationFrom()

    context = {'form': form}
    return render(request, 'registration/sign_up.html', context)