from django.urls import path, include
from rest_framework.routers import DefaultRouter

from team.team_api import views

app_name = "team_api"

router = DefaultRouter()
router.register(r"team", views.TasksViewSet)