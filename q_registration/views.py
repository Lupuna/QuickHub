from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from q_registration import forms as reg_form
from user_project import services as up
from user_project_time import (
    services as upt_services,
    models as upt_models
    )

from . import forms as registration_forms


class PasswordResetCompleteViewCustom(PasswordResetCompleteView):
    template_name = 'q_registration/password_reset_complete.html'


class PasswordResetConfirmViewCustom(PasswordResetConfirmView):
    template_name = 'q_registration/password_reset_confirm.html'
    success_url = reverse_lazy("registration:password_reset_complete")
    form_class = reg_form.CustomSetPasswordForm


class PasswordResetDoneViewCustom(PasswordResetDoneView):
    template_name = 'q_registration/password_reset_done.html'


class PasswordResetViewCustom(PasswordResetView):
    template_name = 'q_registration/password_reset.html'
    email_template_name = 'q_registration/password_reset_email.html'
    success_url = reverse_lazy('q_registration:password_reset_done')
    form_class = reg_form.CustomPasswordResetForm


class LoginCustom(LoginView):
    template_name = "q_registration/sign_in.html"
    form_class = reg_form.AuthenticationFormCustom

    def form_valid(self, form):
        if not form.cleaned_data['remember_me']:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)


def sign_up(request):
    if request.method == 'POST':
        form = registration_forms.CustomUserCreationFrom(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.json_with_settings_info = registration_utils.create_base_settings_json_to_employee()
            user.save()

            up.create_category(user, title='Мои задачи')

            for status in upt_models.UserTimeCategory.Status:
                upt_services.create_time_category(user, status=status)

            login(request, user)
            return redirect(reverse_lazy('team:homepage'))
    else:
        form = registration_forms.CustomUserCreationFrom()

    context = {'form': form}
    return render(request, 'q_registration/sign_up.html', context)