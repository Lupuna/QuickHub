from django.test import TestCase
from django.db.models import QuerySet
from django.utils import timezone

import team.models as team_models
import user_project_time.models as upt_models 
import user_project_time.services as upt_services


class TestServices(TestCase):
    fixtures = ['data.json']

    def setUp(self):
        self.company = team_models.Company.objects.get(id=1)
        self.project = team_models.Project.objects.get(id=1)
        self.user = self.company.employees.first()
        self.task = team_models.Task.objects.first()
        self.executors = self.company.employees.all()

    def test_create_time_category(self):
        time_category = upt_services.create_time_category(user=self.user, status='Test')

        self.assertEqual(time_category.status, 'Test')
        self.assertEqual(time_category.employee, self.user)
        self.assertEqual(time_category.tasks.count(), 0)

    def test_set_user_time_category(self):
        func = lambda task, executors: task

        status = self.task.time_status

        task = upt_services.set_user_time_category(func)(
            task=self.task, 
            executors=self.executors
        )

        task_time_categories = task.time_categories.values_list('id', 'status')
        executors_time_categories = upt_models.UserTimeCategory.objects.filter(
            employee__in=self.executors,
            tasks__in=[task],
        ).values_list('id', 'status')

        self.assertQuerySetEqual(task_time_categories, executors_time_categories, ordered=False)
        self.assertEqual(all([x[1] == status for x in executors_time_categories]), True)