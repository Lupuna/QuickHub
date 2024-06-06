from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden


class AccessMixin:
    '''Базовый миксин обработки доступа'''

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise PermissionDenied
            # return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class CompanyAccessMixin(AccessMixin):
    '''Проверка принадлежности пользователя к запрашиваемой компании'''

    def has_permissions(self):
        return self.kwargs['company_id'] in self.request.user.companies.values_list('id', flat=True)


class ProjectAccessMixin(AccessMixin):
    '''Проверка принадлежности пользователя к проекту'''

    def has_permissions(self):
        if self.kwargs['project'].tasks.exists():
            return self.kwargs['project_id'] in self.request.user.tasks.values_list('project_id', flat=True)
        return True


class TaskAccessMixin(AccessMixin):
    '''Проверка доступа к задаче для пользователя'''

    def has_permissions(self):
        return self.kwargs['task'].project_id.id in self.request.user.tasks.values_list('project_id', flat=True)


class SubtaskAccessMixin(TaskAccessMixin):
    '''Проверка доступа к подзадаче для пользователя'''
