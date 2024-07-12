from rest_framework import serializers

import team.models


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = team.models.Task
        fields = "__all__"