from team.tests.test_base import Settings, SetUpServicesMixin

from user_project_time import models
from user_project_time import services


class TestServices(SetUpServicesMixin, Settings):

    def test_create_time_category(self):
        time_category = services.create_time_category(user=self.employee, status='Test')

        self.assertEqual(time_category.status, 'Test')
        self.assertEqual(time_category.employee, self.employee)
        self.assertEqual(time_category.tasks.count(), 0)

    def test_set_user_time_category(self):
        status = self.task.time_status

        task = services.set_user_time_category(
            task=self.task, 
            executors=self.executors
        )

        task_time_categories = task.time_categories.values_list('id', 'status')
        executors_time_categories = models.UserTimeCategory.objects.filter(
            employee__in=self.executors,
            tasks__in=[task],
        ).values_list('id', 'status')

        self.assertQuerySetEqual(task_time_categories, executors_time_categories, ordered=False)
        self.assertEqual(all([x[1] == status for x in executors_time_categories]), True)