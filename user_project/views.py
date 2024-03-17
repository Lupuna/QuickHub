from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from . import forms as user_project_forms
from team import models as team_models
from . import models as user_project_models

from team import utils as team_utils
from user_project_time import utils as upt_utils 
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


class CreateTaskboard(quickhub_utils.CreatorMixin, LoginRequiredMixin, FormView):
    form_class = user_project_forms.TaskboardCreationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['employee'] = self.request.user
        return kwargs

    def get_initial(self):
        if not self.kwargs.get('category_id'):
            return {}
        category = user_project_models.Category.objects\
            .prefetch_related('tasks')\
            .get(id=self.kwargs['category_id'])
        initial = {
                'category': category, 
                'tasks': category.tasks.all()
            }
        return initial

    def form_valid(self, form):
        tasks = self.request.user.tasks.prefetch_related('subtasks')\
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = self.request.user.categories.prefetch_related(
            'tasks__executors',
            'tasks__subtasks',
            'tasks__project_id__company_id',
            # 'tasks__deadline__time_category',
        )
                                                
        objects = {}
        for cat in categories:
            objects[cat] = cat.tasks.all()
        context['objects'] = objects
        return context

    # def dispatch(self, request, *args, **kwargs):
    #     tasks = request.user.tasks\
    #         .prefetch_related('deadline')\
    #         .distinct()
    #     for task in tasks:
    #         deadline = task.deadline.get(time_category__employee=request.user)
    #         # status = upt_utils.get_deadline_status(deadline)
            
    #     return super().dispatch(request, *args, **kwargs)
