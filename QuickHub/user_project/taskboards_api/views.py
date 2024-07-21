from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from user_project import models
from user_project.taskboards_api import serializers


class CategoryViewSet(ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerialaizer

    def get_queryset(self):
        return self.queryset.filter(employee_id=self.request.user)