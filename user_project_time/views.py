from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView

from team import models as team_models

from . import models as user_project_time_models
from . import services as user_project_time_services


class DeadlineCategoriesListView(LoginRequiredMixin, ListView):
    template_name = 'user_project_time/main_functionality/deadline_taskboard.html'
    context_object_name = 'time_categories'

    def get_queryset(self) -> dict[user_project_time_models.UserTimeCategory, team_models.Task]:
        categories = user_project_time_services.get_user_time_categories(user=self.request.user)
                                                
        objects = {}
        for cat in categories:
            objects[cat] = cat.tasks.all()
        return objects


class DeadlineCategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = 'user_project_time/main_functionality/detail_view.html'
    slug_url_kwarg = 'status'
    context_object_name = 'category'

    def get_object(self, queryset=None):
        slug = self.kwargs[self.slug_url_kwarg]

        category = user_project_time_services.get_user_time_categories(user=self.request.user).get(status=slug)
        return category

