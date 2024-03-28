from django.urls import path
from . import views

app_name = 'user_project'

urlpatterns = [
    path('', views.TaskboardListView.as_view(), name='taskboard'),
    path('create/category', views.CreateCategory.as_view(), name='create_category'),
    path('create/', views.CreateTaskboard.as_view(), name='create_taskboard'),
    path('edit/<int:category_id>/', views.EditTaskboard.as_view(), name='add_task'),
]
