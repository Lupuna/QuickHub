from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

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



