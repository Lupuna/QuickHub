from django.test import TestCase

import team.models as team_models
from user_project import services
from user_project import models


class TestServices(TestCase):
    fixtures = ['data.json']

    def setUp(self):
        self.user = team_models.Employee.objects.get(id=2)
        self.tasks = self.user.tasks.prefetch_related('subtasks').all()
        self.category = models.Category.objects.create(
            title='TEST',
            employee_id=self.user
        )

    def test_create_category(self):
        models.Category.objects.filter(title='TEST').delete()
        
        category = services.create_category(user=self.user, title='TEST')
        
        self.assertEqual(category.title, 'TEST')
        self.assertEqual(category.employee_id, self.user)

    def test_set_tasks_to_category(self):
        self.assertQuerySetEqual(
            self.category.tasks.all(),
            models.Category.objects.none()
        )

        services.set_tasks_to_category(
            category=self.category,
            tasks=self.tasks,
        )

        self.assertQuerySetEqual(
            self.category.tasks.all(),
            self.tasks,    
        )

    def test_create_taskboard_with_tasks(self):
        models.Taskboard.objects.filter(category_id=self.category).delete()

        services.create_taskboards(
            category=self.category, 
            tasks=self.tasks
        )

        for task in self.tasks:
            with self.subTest():
                taskboard = models.Taskboard.objects.get(
                    category_id=self.category,
                    task_id=task,
                )
                self.assertEqual(taskboard.title, self.category.title)
                self.assertEqual(taskboard.task_id, task)
            # for subtask in task.subtasks.only('id', 'text'):
            #     info = taskboard.json_with_subtask_and_subtask_personal_note[subtask.id]

            #     self.assertEqual(info, subtask.text)