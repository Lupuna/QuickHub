from django.urls import path
from . import views

app_name = 'user_project_time'

urlpatterns = [
    path('', views.DeadlineCategoriesListView.as_view(), name='taskboard'),
    # path('category/<slug:status>', ..., name='status_list'),
]
