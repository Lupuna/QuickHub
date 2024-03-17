from django import forms
from . import models as user_project_models
from team import models as team_models


class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = user_project_models.Category
        fields = ('title', 'project_personal_notes')


class TaskboardCreationForm(forms.Form):
    category = forms.ModelChoiceField(queryset=None)
    tasks = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    text = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, employee: team_models.Employee, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = user_project_models.Category.objects.filter(employee_id=employee).all()
        self.fields['tasks'].queryset = employee.tasks.all()