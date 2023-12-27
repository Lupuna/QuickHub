from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'team'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create/company/', views.create_company, name='create_company'),
    # id - это временное решение, ешо нужно будет заменить не токен
    path('create/<int:id>/project/', views.create_project, name='create_project'),
    path('create/<int:company_id>/<int:project_id>/task', views.create_task, name='create_task'),
    path('create/<int:company_id>/<int:project_id>/<int:task_id>/subtask', views.create_subtask, name='create_subtask'),
    path('create/category', views.create_category, name='create_category'),
]
