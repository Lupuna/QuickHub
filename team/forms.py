from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . import utils


class CustomUserCreationFrom(UserCreationForm):
    class Meta:
        model = models.Employee
        fields = ('name', 'username', 'email', 'password1', 'password2')


class CompanyCreationForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = ('title',)


class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ('title', 'view_counter')


class TaskCreationForm(forms.Form):
    title = forms.CharField(max_length=40)
    images = utils.MultipleImageField(required=False)
    text = forms.CharField(widget=forms.Textarea, required=False)
    files = utils.MultipleFileField(required=False)
    responsible = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    executor = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple, required=False)
    parent_id = forms.ModelChoiceField(queryset=None, required=False)

    def __init__(self, company_id, project_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.employee_list = utils.create_employee_list(company_id)
        self.fields['responsible'].queryset = self.employee_list
        self.fields['executor'].queryset = self.employee_list
        self.fields['parent_id'].queryset = models.Project.objects.get(id=project_id).task_set.all()


class SubtaskCreationForm(forms.Form):
    title = forms.CharField(max_length=40)
    images = utils.MultipleImageField(required=False)
    text = forms.CharField(widget=forms.Textarea, required=False)
    files = utils.MultipleFileField(required=False)
    responsible = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    executor = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, company_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.employee_list = utils.create_employee_list(company_id)
        self.fields['responsible'].queryset = self.employee_list
        self.fields['executor'].queryset = self.employee_list


class ChoiceEmployeeParametersForm(forms.Form):
    image = forms.BooleanField(required=False)
    name = forms.BooleanField(required=False)
    email = forms.BooleanField(required=False)
    telephone = forms.BooleanField(required=False)
    position = forms.BooleanField(required=False)


class CreateDepartmentForm(forms.Form):
    title = forms.CharField(max_length=40)
    supervisor = forms.ModelChoiceField(queryset=None)
    parent_id = forms.ModelChoiceField(queryset=None, required=False)

    def __init__(self, company_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supervisor'].queryset = utils.create_employee_list(company_id)
        self.fields['parent_id'].queryset = models.Company.objects.get(id=company_id.id).department_set.all()

