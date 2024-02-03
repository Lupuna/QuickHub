from django import forms
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from . import models


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


class ModifiedFormView(FormView):

    def dispatch(self, request, *args, **kwargs):
        try:
            if self.kwargs.get('company_id'):
                self.kwargs['company_id'] = models.Company.objects.get(id=self.kwargs['company_id'])
            if self.kwargs.get('project_id'):
                self.kwargs['project_id'] = models.Project.objects.get(id=self.kwargs['project_id'])
            if self.kwargs.get('task_id'):
                self.kwargs['task_id'] = models.Task.objects.get(id=self.kwargs['task_id'])
        except ObjectDoesNotExist:
            return redirect(reverse_lazy('team:homepage'))

        return super().dispatch(request, *args, **kwargs)


def create_base_settings_json_to_employee():
    js = {
        "settings_info_about_company_employee": ["image", "name", "email", "telephone", "position_title"]
    }
    return js


def create_employee_list(company_id: int) -> list:
    return models.Employee.objects.filter(
        id__in=models.EmployeeCompany.objects.filter(company_id=company_id).values('employee_id'))


def add_new_employee(company_id, employee_id):
    company_id = models.Company.objects.get(id=company_id)
    employee_id = models.Employee.objects.get(id=employee_id)
    new_employee = models.EmployeeCompany(company_id=company_id, employee_id=employee_id)
    new_employee.save()
