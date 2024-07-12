from rest_framework.viewsets import ModelViewSet

import user_project_time.models
from user_project_time.deadlines_api import serializers


class DeadlinesViewSet(ModelViewSet):
    queryset = user_project_time.models.UserTimeCategory.objects.all()
    serializer_class = serializers.DeadlineSerializer