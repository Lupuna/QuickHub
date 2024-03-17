from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages


class CompanyAccess(LoginRequiredMixin):
    '''Проверка принадлежности пользователя к запрашиваемой компании'''
    def dispatch(self, request, *args, **kwargs):
        try:
            company = self.kwargs['company']
        except ObjectDoesNotExist:
            messages.error(request, 'Access denied')
            return redirect(reverse_lazy('team:homepage'))

        if company not in request.user.companies.all():
            return redirect(reverse_lazy('team:homepage'))
        return super().dispatch(request, *args, **kwargs)
