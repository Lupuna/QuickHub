from rest_framework import serializers

import user_project.models


class CategorySerialaizer(serializers.ModelSerializer):
    class Meta:
        model = user_project.models.Category
        fields = "__all__"