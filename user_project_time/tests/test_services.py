from django.test import TestCase
from django.utils import timezone

from team import models as team_models
from .. import models as upt_models 
from .. import services


# class TestServices(TestCase):
#     def setUp(self) -> None:
#         team_models.Employee.objects.create(
#             username='User',
#             email='user@user.py'
#         )

#         team_models.Task.objects.create(
#             title='Task',
#             project_id=project
#         )

#     def test_update_deadline_status(self):
#         user = team_models.Employee.objects.create()
#         task = team_models.Task.objects.get(id=26)

#         time_end = timezone.now()

#         deadline = services.update_deadline(user=user, task=task, end=time_end)
        
#         self.assertEqual(deadline.time_end, time_end)
#         self.assertEqual(deadline.time_category.status, 'Overtimed')