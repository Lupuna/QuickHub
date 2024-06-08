from team.tests.test_base import Settings
import team
from user_project import services
from user_project import models


class TestServices(Settings):

    def setUp(self):
        super().setUp()
        self.category = models.Category.objects.create(
            title="TEST-category",
            employee_id=self.employee
        )
        self.task1 = self._create_task(1)
        self.task2 = self._create_task(2)
        self.task3 = self._create_task(3)

        self.tasks = self.project.tasks.all()

    def _create_task(self, id: int):
        return team.models.Task.objects.create(
            title=f"task_test{id}",
            project_id=self.project
        )

    def test_create_category(self):
        """Проверка создания категории для пользователя"""
        models.Category.objects.filter(title='TEST').delete()
        
        category = services.create_category(user=self.employee, title='TEST')
        
        self.assertEqual(category.title, 'TEST')
        self.assertEqual(category.employee_id, self.employee)

    def test_set_tasks_to_category(self):
        """Проверка назначения задач в нужную категорию"""
        self.assertQuerySetEqual(
            self.category.tasks.all(),
            models.Category.objects.none(),
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
        """Проверка создания досок с задачами для нужной категории"""
        models.Taskboard.objects.filter(category_id=self.category).delete()

        services.create_taskboards(
            category=self.category, 
            tasks=self.tasks
        )

        for task in self.tasks:
            with self.subTest("Проверка создания записей в таблице Taskboard"):
                taskboard = models.Taskboard.objects.get(
                    category_id=self.category,
                    task_id=task,
                )
                self.assertEqual(taskboard.title, self.category.title)
                self.assertEqual(taskboard.task_id, task)
            # for subtask in task.subtasks.only('id', 'text'):
            #     info = taskboard.json_with_subtask_and_subtask_personal_note[subtask.id]

            #     self.assertEqual(info, subtask.text)