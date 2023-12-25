from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


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
    images = MultipleImageField(required=False)
    text = forms.CharField(widget=forms.Textarea, required=False)
    files = MultipleFileField(required=False)
    responsible = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    executor = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple, required=False)
    parent_id = forms.ModelChoiceField(queryset=None, required=False)

    def __init__(self, company_id, project_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.employee_list = models.Employee.objects.filter(
            id__in=models.EmployeeCompany.objects.filter(company_id=company_id).values('employee_id'))
        self.fields['responsible'].queryset = self.employee_list
        self.fields['executor'].queryset = self.employee_list
        self.fields['parent_id'].queryset = models.Project.objects.get(id=project_id).task_set.all()


class SubtaskCreationForm(forms.Form):
    title = forms.CharField(max_length=40)
    images = MultipleImageField(required=False)
    text = forms.CharField(widget=forms.Textarea, required=False)
    files = MultipleFileField(required=False)
    responsible = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    executor = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, company_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.employee_list = models.Employee.objects.filter(
            id__in=models.EmployeeCompany.objects.filter(company_id=company_id).values('employee_id'))
