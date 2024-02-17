from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.shortcuts import redirect

from . import models


class CompanyAccess(LoginRequiredMixin):
    '''Проверка принадлежности пользователя к запрашиваемой компании'''
    def dispatch(self, request, *args, **kwargs):
        try:
            company = models.Company.objects.get(id=self.kwargs['company_id'])
        except TypeError:
            company = self.kwargs['company_id']
        except ObjectDoesNotExist:
            return redirect(reverse_lazy('team:homepage'))

        if company not in request.user.companies.all():
            return redirect(reverse_lazy('team:homepage'))
        return super().dispatch(request, *args, **kwargs)
