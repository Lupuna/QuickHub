from datetime import datetime
from django.db.models import Q
from rest_framework import viewsets
from api import serializers
from team import models
from django.conf import settings
import pytz


class CompanyEventAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CompanySerializer

    def get_queryset(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        datetime_start = tz.localize(datetime.strptime(self.kwargs['datetime_start'], '%Y-%m-%dT%H:%M'))
        datetime_end = tz.localize(datetime.strptime(self.kwargs['datetime_end'], '%Y-%m-%dT%H:%M'))

        return models.CompanyEvent.objects.filter(
            Q(time_start__gte=datetime_start) & Q(time_end__lte=datetime_end) & Q(company=self.kwargs['company'])
        ).select_related('company').prefetch_related('images', 'files')
