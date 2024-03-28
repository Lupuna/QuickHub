from django.urls import path, include
from . import views

app_name = 'team'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    # создание
    path('create/company/', views.CreateCompany.as_view(), name='create_company'),
    path('create/<int:company_id>/project/', views.CreateProject.as_view(), name='create_project'),
    path('create/<int:company_id>/<int:project_id>/task', views.CreateTask.as_view(), name='create_task'),
    path('create/<int:company_id>/<int:project_id>/<int:task_id>/subtask', views.CreateSubtask.as_view(), name='create_subtask'),
    path('create/<int:company_id>/department', views.CreateDepartment.as_view(), name='create_department'),
    path('create/<int:company_id>/position', views.CreatePosition.as_view(), name='create_position'),
    path('create/<int:company_id>/company-event', views.CreateCompanyEvent.as_view(), name='create_company_event'),
    # отображение
    path('<int:company_id>/check-employee', views.CheckEmployee.as_view(), name='check_employee'),
    path('<int:company_id>/check-employee/choice-parameters', views.ChoiceParameters.as_view(), name='choice_parameters'),
    path('profile', views.UserProfileListView.as_view(), name='user_profile'),
    # Детальные отображения
    path('company/<int:company_id>/', views.CompanyDetailView.as_view(), name='company'),
    path('<int:company_id>/project/<int:project_id>/', views.ProjectDetailView.as_view(), name='project'),
    path('<int:company_id>/department/<int:department_id>/', views.DepartmentDetailView.as_view(), name='department'),
    path('<int:company_id>/position/<int:position_id>/', views.PositionDetailView.as_view(), name='position'),
    path('<int:company_id>/<int:project_id>/<int:task_id>/', views.TaskDetailView.as_view(), name='task'),
    path('<int:company_id>/<int:project_id>/<int:task_id>/<int:subtask_id>', views.SubtaskDetailView.as_view(), name='subtask'),
    # Списки
    path('<int:company_id>/projects/', views.ProjectsListView.as_view(), name='projects_list'),
    path('<int:company_id>/positions/', views.PositionsListView.as_view(), name='positions_list'),
    path('<int:company_id>/departments/', views.DepartmentsListView.as_view(), name='departments_list'),
    path('companies/', views.UserCompaniesListView.as_view(), name='companies'),
    path('projects/', views.UserProjectsListView.as_view(), name='projects'),
    # Редактирование
    path('edit/<int:company_id>/<int:project_id>/<int:task_id>/', views.TaskUpdateView.as_view(), name='task_update'),
    # Изменение
    path('profile/<int:pk>/update', views.UpdateUserProfile.as_view(), name='update_user_profile'),
    path('profile/password', views.UserPasswordChangeView.as_view(), name='change_password'),

    # ещё не готово
    path('settings/', views.homepage, name='settings'),
    path('help/', views.homepage, name='help'),
    path('me/', views.homepage, name='me'),
    path('chat/', views.homepage, name='chat'),
    path('notifications/', views.homepage, name='notifications'),
]
