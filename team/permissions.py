from django.urls import reverse_lazy
from django.contrib import messages


class AccessMixin:
    '''Базовый миксин обработки доступа'''
    login_url = reverse_lazy('q_registration:login')

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
        return self.kwargs['task'].project_id.id in self.request.user.tasks.values_list('project_id', flat=True)


class SubtaskAccessMixin(TaskAccessMixin):
    '''Проверка доступа к подзадаче для пользователя'''
