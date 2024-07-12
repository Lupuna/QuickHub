import logging

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from team.models import Task, Project, Employee
from team.team_api.serializers import TaskSerializer


logger = logging.getLogger(__name__)


class TasksViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        logger.info(self.request.user.name)
        return self.request.user.tasks.all()