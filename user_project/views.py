from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from . import forms as user_project_forms
from team import models as team_models
from . import models as user_project_models
from team import utils as team_utils
from QuickHub import utils as quickhub_utils


class CreateCategory(quickhub_utils.CreatorMixin, LoginRequiredMixin, FormView):
    form_class = user_project_forms.CategoryCreationForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.success_url = reverse_lazy('user_project:taskboard')

    def form_valid(self, form):
        try:
            category = form.save(commit=False)
            category.title = form.cleaned_data.get('title')
            category.employee_id = team_models.Employee.objects.get(id=self.request.user.id)
            category.project_personal_notes = form.cleaned_data.get('project_personal_notes')
            category.save()
        except:
            return redirect(reverse_lazy('user_project:create_category'))
        return super().form_valid(category)


class CreateTaskboard(quickhub_utils.ModifiedDispatch, LoginRequiredMixin, FormView):
    form_class = user_project_forms.TaskboardCreationForm

    def dispatch(self, request, *args, **kwargs):
        try:
            self.kwargs['user'] = team_models.Employee.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
            return redirect(reverse_lazy('team:homepage'))
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['emp_id'] = self.kwargs['user'].id
        return kwargs

    def form_valid(self, form):
        tasks = self.kwargs['user'].tasks \
            .filter(id__in=form.cleaned_data.get('tasks'))
        category = form.cleaned_data.get('category')

        for task in tasks:
            taskboard = user_project_models.Taskboard(
                category_id=category,
                task_id=task,
                title=category.title,
                task_personal_notes={
                  'notes': form.cleaned_data.get('text'),
                  'task_notes': task.text
                }
            )
            subtasks = task.subtasks.all()
            for subtask in subtasks:
                taskboard.json_with_subtask_and_subtask_personal_note[subtask.id] = subtask.text
            taskboard.save()
        return super().form_valid(form)


class TaskboardListView(LoginRequiredMixin, ListView):
    model = team_models.Employee
    template_name = 'user_project/main_functionality/taskboard.html'

    def dispatch(self, request, *args, **kwargs):
        tasks = request.user.tasks.distinct()
        for task in tasks:
            deadline = task.deadlines.get()
            deadline.status = team_utils.get_deadline_status(deadline)
            deadline.save()
        return super().dispatch(request, *args, **kwargs)
