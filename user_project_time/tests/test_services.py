from django.test import TestCase
from django.utils import timezone

from team import models as team_models
from .. import models as upt_models 
from .. import services


class TestServices(TestCase):
    def test_update_deadline_status(self):
        user = team_models.Employee.objects.get(id=1)
        task = team_models.Task.objects.get(id=1)

        time_end = timezone.now()

        deadline = services.update_deadline(user=user, task=task, end=time_end)
        
        self.assertEqual(deadline.time_end, time_end)
        self.assertEqual(deadline.time_category.status, 'Overtimed')