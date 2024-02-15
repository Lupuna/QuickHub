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
    path('create/<int:company_id>/<int:project_id>/task', views.CreateTask.as_view(), name='create_task'),
    path('create/<int:company_id>/<int:project_id>/<int:task_id>/subtask', views.CreateSubtask.as_view(), name='create_subtask'),
    path('create/category', views.CreateCategory.as_view(), name='create_category'),
    path('create/<int:company_id>/department', views.CreateDepartment.as_view(), name='create_department'),
    path('create/taskboard', views.CreateTaskboard.as_view(), name='create_taskboard'),
    path('create/<int:company_id>/department', views.CreateDepartment.as_view(), name='create_department'),
    path('create/<int:company_id>/<int:project_id>/task', views.CreateTask.as_view(), name='create_task'),
    path('create/<int:company_id>/<int:project_id>/<int:task_id>/subtask', views.CreateSubtask.as_view(), name='create_subtask'),
    path('create/category', views.CreateCategory.as_view(), name='create_category'),
    path('create/<int:company_id>/position', views.CreatePosition.as_view(), name='create_position'),
    path('create/<int:company_id>/company-event', views.CreateCompanyEvent.as_view(), name='create_company_event'),
    # отображение
    path('<int:company_id>/check-employee', views.CheckEmployee.as_view(), name='check_employee'),
    path('<int:company_id>/check-employee/choice-parameters', views.ChoiceParameters.as_view(), name='choice_parameters'),
    path('<int:company_id>/department/<int:department_id>', views.view_department, name='department'),
    path('taskboard', views.taskboard, name='taskboard'),
    path('<int:company_id>/projects/', views.ProjectsView.as_view(), name='projects_list'),
    path('<int:company_id>/positions/', views.PositionsView.as_view(), name='positions_list'),
    path('<int:company_id>/departments/', views.DepartmentsView.as_view(), name='departments_list'),

    # ещё не готово
    path('projects/', views.homepage, name='projects'),
    path('companies/', views.homepage, name='companies'),
    path('settings/', views.homepage, name='settings'),
    path('help/', views.homepage, name='help'),
    path('me/', views.homepage, name='me'),
    path('chat/', views.homepage, name='chat'),
    path('notifications/', views.homepage, name='notifications'),
]
