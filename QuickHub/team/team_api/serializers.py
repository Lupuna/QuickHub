from rest_framework import serializers

from team import models


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ('id', 'title', 'owner_id')


class CompanyEventFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CompanyEventFile
        fields = '__all__'


class CompanyEventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyEventImage
        fields = '__all__'


class CompanyEventSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    files = CompanyEventFileSerializer(many=True)
    images = CompanyEventImageSerializer(many=True)

    class Meta:
        model = models.CompanyEvent
        fields = (
            'id', 'title', 'description',
            'json_with_employee_info', 'time_start',
            'time_end', 'company', 'files', 'images'
        )

