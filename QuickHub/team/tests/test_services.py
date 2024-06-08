from django.utils import timezone

import team.forms
import user_project.models
from team.services import tasks_service
import team.models as team_models
import team.forms as team_forms
import user_project_time.models as user_project_time_models
from team.tests.test_base import Settings, SetUpServicesMixin


class TestServices(SetUpServicesMixin, Settings):

    def test_employee_info(self):
        appoints = ('TEST', ['TEST'], self.employee)
        
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

    def test_update_task_deadline_START_END_ARE_NONE(self):

        task = tasks_service.update_task_deadline(
            task=self.task,
            start=None,
            end=None
        )
        self.assertNotEqual(task.time_start, None)
        self.assertEqual(task.time_end, None)

    def test_update_task_deadline_START_NOT_NONE_END_IS_NONE(self):
        start = timezone.now()

        task = tasks_service.update_task_deadline(
            task=self.task,
            start=start,
            end=None
        )
        self.assertEqual(task.time_start, start)
        self.assertEqual(task.time_end, None)

    def test_update_task_deadline_START_IS_NONE_END_NOT_NONE(self):
        end = timezone.now() + timezone.timedelta(days=1)

        task = tasks_service.update_task_deadline(
            task=self.task,
            end=end,
        )
        self.assertNotEqual(task.time_start, None)
        self.assertEqual(task.time_end, end)

        self.assertEqual(
            task.time_status, 
            user_project_time_models.UserTimeCategory.Status.TODAY
        )

    def test_update_task_deadline_START_END_ARE_NOT_NONE(self):
        start = timezone.now()
        end = start + timezone.timedelta(days=30)

        task = tasks_service.update_task_deadline(
            task=self.task,
            start=start,
            end=end
        )
        self.assertEqual(task.time_start, start)
        self.assertEqual(task.time_end, end)

        self.assertEqual(
            task.time_status, 
            user_project_time_models.UserTimeCategory.Status.MONTH
        )

    def test_update_task(self):
        data = {
            "title": "Task_test",
            "text": "Here is some text",
            "time_start": timezone.now(),
            "time_end": timezone.now() + timezone.timedelta(days=2),
            "executors": self.executors,
        }
        form = team.forms.TaskCreationForm(
            company_id=self.company,
            project_id=self.project,
            data=data
        )
        form.is_valid()

        task = tasks_service.update_task(
            task=self.task,
            form=form
        )

        with self.subTest("Изменение названия"):
            self.assertEqual(data["title"], task.title)

        with self.subTest("Изменение текста"):
            self.assertEqual(data["text"], task.text)

        with self.subTest("Изменение времени начала"):
            self.assertEqual(data["time_start"], task.time_start)

        with self.subTest("Изменение времени конца срока"):
            self.assertEqual(data["time_end"], task.time_end)

        with self.subTest("Изменение исполнителей"):
            self.assertQuerySetEqual(data["executors"], task.executors.all(), ordered=True)

        for employee in self.executors:
            with self.subTest("Назначение задачи в категорию 'Мои задачи' для исполнителей"):
                user_category = employee.categories.get(taskboards__task_id=task)
                self.assertEqual(user_category.title, 'Мои задачи')

                task_category = task.user_category.get(employee_id=employee)
                self.assertEqual(user_category, task_category)

            with self.subTest("Назначение задачи в нужную категорию срочности для исполнителей"):
                user_time_category = employee.time_categories.get(deadlines__task=task)
                self.assertEqual(user_time_category.status, task.time_status)

                task_time_category = task.time_categories.get(employee=employee)
                self.assertEqual(user_time_category, task_time_category)

