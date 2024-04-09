from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

from QuickHub.utils import ModifiedDispatch


class AccessMixin(ModifiedDispatch, LoginRequiredMixin):
    '''Базовый миксин обработки доступа'''

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise PermissionError('Нет доступа')
        return super().dispatch(request, *args, **kwargs)


class CompanyAccessMixin(AccessMixin):
    '''Проверка принадлежности пользователя к запрашиваемой компании'''

    def has_permissions(self):
        return self.kwargs['company_id'] in self.request.user.companies.values_list('id', flat=True)


class ProjectAccessMixin(AccessMixin):
    '''Проверка принадлежности пользователя к проекту'''

    def has_permissions(self):
        return self.kwargs['project_id'] in self.request.user.tasks.values_list('project_id', flat=True)


class TaskAccessMixin(AccessMixin):
    '''Проверка доступа к задаче для пользователя'''

    def has_permissions(self):
        # return self.kwargs['task'].project_id in self.request.user.tasks.values_list('project_id', flat=True)
        return True


class SubtaskAccessMixin(AccessMixin):
    '''Проверка доступа к подзадаче для пользователя'''

    def has_permissions(self):
        return True
