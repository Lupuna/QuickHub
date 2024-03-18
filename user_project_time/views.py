from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView

from team import models as team_models

from . import models as user_project_time_models


class DeadlineCategoriesListView(LoginRequiredMixin, ListView):
    model = team_models.Employee
    template_name = 'user_project_time/main_functionality/deadline_taskboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = self.request.user.time_categories.prefetch_related(
            'tasks__executors',
            'tasks__subtasks',
            'tasks__project_id__company_id',
            'tasks__deadline__time_category',
        )
                                                
        objects = {}
        for cat in categories:
            objects[cat] = cat.tasks.all()
        context['objects'] = objects
        return context


class DeadlineCategoryDetailView(LoginRequiredMixin, DetailView):
    model = user_project_time_models.UserTimeCategory
    template_name = 'user_project_time/main_functionality/detail_view.html'
    slug_url_kwarg = 'status'
    context_object_name = 'category'

    def get_object(self, queryset=None):
        slug = self.kwargs[self.slug_url_kwarg]
        
        category = self.request.user.time_categories.prefetch_related(
            'tasks__executors',
            'tasks__subtasks',
            'tasks__project_id__company_id',
            'tasks__deadline__time_category',
        ).get(status=slug)
        return category

