from django import forms
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from . import models

creator = 'team/main_functionality/includes/creator.html'


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
            if self.kwargs.get('company_id'):
                self.kwargs['company'] = models.Company.objects.get(id=self.kwargs['company_id'])
            if self.kwargs.get('project_id'):
                self.kwargs['project'] = models.Project.objects.get(id=self.kwargs['project_id'])
            if self.kwargs.get('task_id'):
                self.kwargs['task'] = models.Task.objects.get(id=self.kwargs['task_id'])
            if self.kwargs.get('category_id'):
                self.kwargs['category'] = models.Category.objects.get(id=self.kwargs['category_id'])
        except ObjectDoesNotExist:
            return redirect(reverse_lazy('team:homepage'))

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.kwargs.get('company'):
            context['company'] = self.kwargs.get('company')
        if self.kwargs.get('project'):
            context['project'] = self.kwargs.get('project')
        if self.kwargs.get('task'):
            context['task'] = self.kwargs.get('task')
        if self.kwargs.get('category'):
            context['category'] = self.kwargs.get('category')
        return context
    

class CreatorMixin:
    def __init__(self, *args, **kwargs):
        self.template_name = creator
        self.success_url = reverse_lazy('team:homepage')
        self.login_url = reverse_lazy('team:login')
        self.extra_context = {'title': f'QuickHub: {self.__class__.__name__.replace("Create", "")}-create'}


def create_base_settings_json_to_employee():
    js = {
        "settings_info_about_company_employee": ["image", "name", "email", "telephone", "position_title"]
    }
    return js


def add_new_employee(company_id, employee_id):
    company_id = models.Company.objects.get(id=company_id)
    employee_id = models.Employee.objects.get(id=employee_id)
    new_employee = models.EmployeeCompany(company_id=company_id, employee_id=employee_id)
    new_employee.save()


def set_position(employee_id, company_id, position_id):
    user = models.Employee.objects.get(id=employee_id)
    position = models.Positions.objects.get(id=position_id)
    company = models.Company.objects.get(id=company_id)
    employee = models.EmployeeCompany.objects.get(employee_id=user, company_id=company)
    employee.position_id = position
    employee.save()


def get_deadline_status(deadline):
    time_end = deadline.time_end
    now = timezone.now()
    if time_end is None:
        return 'Permanent'

    time_interval = (time_end - now).total_seconds()
    day = 86400     # sec

    if time_interval < 0:
        return 'Overtimed'
    elif time_interval <= day:
        return 'Today'
    elif time_interval <= 2 * day:
        return 'Tomorrow'
    elif time_interval <= 7 * day:
        return 'Week'
    elif time_interval <= 30 * day:
        return 'Month'
    else:
        return 'Not_soon'