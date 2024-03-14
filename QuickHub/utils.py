from django import forms
from team import models as team_models
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.shortcuts import redirect


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ModifiedDispatch:
    def dispatch(self, request, *args, **kwargs):
        try:
            if self.kwargs.get('company_id') and self.kwargs.get('project_id') and self.kwargs.get('task_id'):
                self.kwargs['project'] = team_models.Project.objects.select_related('company_id').get(id=self.kwargs['project_id'])
                self.kwargs['company'] = self.kwargs['project'].company_id
                self.kwargs['task'] = self.kwargs['project'].tasks.get(id=self.kwargs['task_id'])
            elif self.kwargs.get('company_id') and self.kwargs.get('project_id'):
                self.kwargs['project'] = team_models.Project.objects.select_related('company_id').get(id=self.kwargs['project_id'])
                self.kwargs['company'] = self.kwargs['project'].company_id            
            elif self.kwargs.get('company_id'):
                self.kwargs['company'] = team_models.Company.objects.get(id=self.kwargs['company_id'])
        except ObjectDoesNotExist:
            return redirect(reverse_lazy('team:homepage'))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['company'] = self.kwargs.get('company')
        context['project'] = self.kwargs.get('project')
        context['task'] = self.kwargs.get('task')
        return context


creator = 'includes/creator.html'


class CreatorMixin:
    def __init__(self, *args, **kwargs):
        self.template_name = creator
        self.success_url = reverse_lazy('team:homepage')
        self.login_url = reverse_lazy('team:login')
        self.extra_context = {'title': f'QuickHub: {self.__class__.__name__.replace("Create", "")}-create'}
