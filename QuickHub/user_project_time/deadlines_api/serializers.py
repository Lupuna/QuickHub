from rest_framework import serializers

import user_project_time.models


class DeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_project_time.models.UserTimeCategory
        fields = "__all__"