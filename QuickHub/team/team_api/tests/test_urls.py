from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from APIs.core.test_base import APISettings

from team import models
from user_project import models


# class TeamAPITests(APISettings):
#
#     def test_get_tasks_GUEST_USER(self):
#         project_id = self.project.id
#         response = self.client.get(reverse("task-list", args=[project_id, ]))
#
#         self.assertEqual(response.status_code, status.HTTP_302_FOUND)