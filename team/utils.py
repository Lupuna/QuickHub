from django import forms
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy, reverse
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
        except ObjectDoesNotExist:
            return redirect(reverse_lazy('team:homepage'))

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['company'] = self.kwargs.get('company')
        context['project'] = self.kwargs.get('project')
        context['task'] = self.kwargs.get('task')
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


def create_employee_list(company_id: int) -> list:
    # return models.Employee.objects.filter(
    #     id__in=models.EmployeeCompany.objects.filter(company_id=company_id).values('employee_id'))
    return company_id.employees.all()


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