from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'team'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    # авторизация
    path('sign-up/', views.sign_up, name='sign_up'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # создание
    path('create/company/', views.CreateCompany.as_view(), name='create_company'),
    path('create/<int:company_id>/project/', views.CreateProject.as_view(), name='create_project'),
    path('create/<int:company_id>/department', views.create_department, name='create_department'),
    path('create/<int:company_id>/<int:project_id>/task', views.CreateTask.as_view(), name='create_task'),
    path('create/<int:company_id>/<int:project_id>/<int:task_id>/subtask', views.CreateSubtask.as_view(), name='create_subtask'),
    path('create/category', views.CreateCategory.as_view(), name='create_category'),
    path('create/<int:company_id>/department', views.create_department, name='create_department'),
    path('create/taskboard', views.create_taskboard, name='create_taskboard'),
    path('create/<int:company_id>/position', views.CreatePosition.as_view(), name='create_position'),
    # отображение
    path('<int:company_id>/check-employee', views.check_employee, name='check_employee'),
    path('<int:company_id>/check-employee/choice-parameters', views.ChoiceParameters.as_view(), name='choice_parameters'),
    path('<int:company_id>/positions', views.view_positions, name='positions'),
    path('<int:company_id>/department/<int:department_id>', views.view_department, name='department'),
    path('taskboard', views.taskboard, name='taskboard'),
]
