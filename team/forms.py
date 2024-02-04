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
        self.employee_list = utils.create_employee_list(company_id=company_id)
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
        self.employee_list = utils.create_employee_list(company_id=company_id)
        self.fields['responsible'].queryset = self.employee_list
        self.fields['executor'].queryset = self.employee_list


class ChoiceEmployeeParametersForm(forms.Form):
    image = forms.BooleanField(required=False)
    name = forms.BooleanField(required=False)
    email = forms.BooleanField(required=False)
    telephone = forms.BooleanField(required=False)
    position_title = forms.BooleanField(required=False)
    department = forms.BooleanField(required=False)


class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = models.UserProject
        fields = ('title', 'project_personal_notes')


class TaskboardCreationForm(forms.Form):
    category = forms.ModelChoiceField(queryset=None)
    tasks = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    text = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, emp_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = models.UserProject.objects.filter(employee_id=emp_id).all()
        self.fields['tasks'].queryset = models.Employee.objects.get(id=emp_id).tasks.all()


class DepartmentCreationForm(forms.Form):
    title = forms.CharField(max_length=40)
    parent = forms.ModelChoiceField(queryset=None, required=False)
    supervisor = forms.ModelChoiceField(queryset=None, required=True)
    employees = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple, required=True)

    def __init__(self, company_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.employee_list = utils.create_employee_list(company_id=company_id)
        self.fields['parent'].queryset = models.Department.objects.filter(company_id=company_id)
        self.fields['supervisor'].queryset = self.employee_list
        self.fields['employees'].queryset = self.employee_list


class PositionCreationForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = models.Positions
        fields = ('title', 'weight',)


class CompanyEventCreationForm(forms.Form):
    title = forms.CharField(max_length=40)
    images = utils.MultipleImageField(required=False)
    files = utils.MultipleImageField(required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    date = forms.DateField()
    time_start = forms.TimeField()
    time_end = forms.TimeField()
    present_employees = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, company_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['present_employees'] = utils.create_employee_list(company_id=company_id)

