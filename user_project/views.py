from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from django.db.models import F
from django.db import IntegrityError

from team import models as team_models
from team import utils as team_utils

from . import forms as user_project_forms
from . import models as user_project_models
from . import services as user_project_services 

from user_project_time import utils as user_project_time_utils 
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
            category.employee_id = self.request.user
            category.project_personal_notes = form.cleaned_data.get('project_personal_notes')
            category.save()
        except:
            return redirect(reverse_lazy('user_project:create_category'))
        return super().form_valid(category)


class CreateTaskboard(quickhub_utils.CreatorMixin, LoginRequiredMixin, FormView):
    form_class = user_project_forms.TaskboardCreationForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.success_url = reverse_lazy('user_project:taskboard')
        
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
        tasks = form.cleaned_data.get('tasks')
        category = form.cleaned_data.get('category')
        notes = form.cleaned_data.get('text')

        try:
            user_project_services.create_taskboard(
                category=category,
                tasks=tasks,
                notes=notes,
            )
        except IntegrityError:
            return redirect('user_project:add_task', 
                            category_id=self.kwargs['category_id'])
        return super().form_valid(form)


class TaskboardListView(LoginRequiredMixin, ListView):
    template_name = 'user_project/main_functionality/taskboard.html'
    context_object_name = 'categories'

    def get_queryset(self) -> dict[user_project_models.Category, team_models.Task]:
        categories = user_project_services.get_user_categories(user=self.request.user)
                                                
        objects = {}
        for cat in categories:
            objects[cat] = cat.tasks.all()
        return objects
