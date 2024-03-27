from django.test import TestCase
from django.utils import timezone

from team.services import tasks_service
import team.models as team_models
import team.forms as team_forms
import user_project_time.models as user_project_time_models


class TestServices(TestCase):
    fixtures = ['data.json']
    
    def setUp(self):
        self.user = team_models.Employee.objects.get(username='User 13')
        self.task = team_models.Task.objects.get(id=36)
        self.project = self.task.project_id
        self.company = self.project.company_id
        self.executors = self.company.employees.all()

    def test_employee_info(self):
        appoints = ('TEST', ['TEST'], self.user)
        
        for appoint in appoints:
            with self.subTest():
                data = {
                    'title': 'TEST',
                    'text': 'TEST',
                    'responsible': self.executors[:3],
                    'executor': self.executors,
                }
                form = team_forms.TaskCreationForm(
                    company_id=self.company,
                    project_id=self.project,
                    data=data,
                )

                self.assertTrue(form.is_valid())

                info = tasks_service.employee_info(
                    task=self.task,
                    form=form,
                    appoint=appoint
                )
                self.assertIsInstance(info['appoint'], list)
                
                # self.assertEqual(info['appoint'], )
                self.assertEqual(info['responsible'], list(self.executors.values_list('email', flat=True)[:3]))
                self.assertEqual(info['executor'], list(self.executors.values_list('email', flat=True)))

    def test_set_executors(self):
        self.task.executors.clear()

        self.assertQuerySetEqual(
            self.task.executors.all(), 
            team_models.Employee.objects.none()
        )

        task = tasks_service.set_executors(
            task=self.task,
            executors=self.executors
        )

        executors = task.executors.all()
        self.assertQuerySetEqual(executors, self.executors, ordered=False)

        for employee in executors:
            with self.subTest():
                user_category = employee.categories.get(taskboards__task_id=task)
                self.assertEqual(user_category.title, 'Мои задачи')

                task_category = task.user_category.get(employee_id=employee)
                self.assertEqual(user_category, task_category)

            with self.subTest():
                user_time_category = employee.time_categories.get(deadlines__task=task)
                self.assertEqual(user_time_category.status, task.time_status)

                task_time_category = task.time_categories.get(employee=employee)
                self.assertEqual(user_time_category, task_time_category)

    def test_update_task_deadline_START_END_ARE_NONE(self):

        # start = None, end = None
        task = tasks_service.update_task_deadline(
            task=self.task,
            executors=self.executors
        )
        self.assertNotEqual(task.time_start, None)
        self.assertEqual(task.time_end, None)

        for employee in self.executors:
            with self.subTest():
                user_time_category = employee.time_categories.get(deadlines__task=task)
                self.assertEqual(user_time_category.status, task.time_status)

                task_time_category = task.time_categories.get(employee=employee)
                self.assertEqual(user_time_category, task_time_category)

    def test_update_task_deadline_START_NOT_NONE_END_IS_NONE(self):
        start = timezone.datetime(2024, 3, 10, 13, 17, 26, 134531, tzinfo=timezone.utc)

        task = tasks_service.update_task_deadline(
            task=self.task,
            executors=self.executors,
            start=start
        )
        self.assertEqual(task.time_start, start)
        self.assertEqual(task.time_end, None)

        for employee in self.executors:
            with self.subTest():
                user_time_category = employee.time_categories.get(deadlines__task=task)
                self.assertEqual(user_time_category.status, task.time_status)

                task_time_category = task.time_categories.get(employee=employee)
                self.assertEqual(user_time_category, task_time_category)

    def test_update_task_deadline_START_IS_NONE_END_NOT_NONE(self):
        end = timezone.datetime(2024, 3, 10, 13, 17, 26, 134531, tzinfo=timezone.utc)

        task = tasks_service.update_task_deadline(
            task=self.task,
            executors=self.executors,
            end=end,
        )
        self.assertNotEqual(task.time_start, None)
        self.assertEqual(task.time_end, end)

        self.assertEqual(
            task.time_status, 
            user_project_time_models.UserTimeCategory.Status.OVERTIMED
        )

        for employee in self.executors:
            with self.subTest():
                user_time_category = employee.time_categories.get(deadlines__task=task)
                self.assertEqual(user_time_category.status, task.time_status)

                task_time_category = task.time_categories.get(employee=employee)
                self.assertEqual(user_time_category, task_time_category)

    def test_update_task_deadline_START_END_ARE_NOT_NONE(self):
        start = timezone.datetime(2024, 3, 10, 13, 17, 26, 134531, tzinfo=timezone.utc)
        end = timezone.datetime(2024, 4, 10, 13, 17, 26, 134531, tzinfo=timezone.utc)

        task = tasks_service.update_task_deadline(
            task=self.task,
            executors=self.executors,
            start=start,
            end=end
        )
        self.assertEqual(task.time_start, start)
        self.assertEqual(task.time_end, end)

        self.assertEqual(
            task.time_status, 
            user_project_time_models.UserTimeCategory.Status.MONTH
        )
        for employee in self.executors:
            with self.subTest():
                user_time_category = employee.time_categories.get(deadlines__task=task)
                self.assertEqual(user_time_category.status, task.time_status)

                task_time_category = task.time_categories.get(employee=employee)
                self.assertEqual(user_time_category, task_time_category)

    