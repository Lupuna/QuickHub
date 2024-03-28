from django.core.exceptions import ValidationError
from django.utils import timezone
from .test_base import Settings
from team import models as test_models
from django.urls import reverse


class TestEmployeeModel(Settings):
    def setUp(self):
        self.test_link = test_models.LinksResources.objects.create(
            employee_id=self.employee,
            title='test_title_1',
            link='https://store.steampowered.com/app/1337520/Risk_of_Rain_Returns/'
        )

    def test_str_method_employee(self):
        self.assertEqual(self.employee.email, str(self.employee))

    def test_get_all_info_method_employee(self):
        employee_info = {
            'image': self.employee.image,
            'name': self.employee.name,
            'email': self.employee.email,
            'city': self.employee.city,
            'birthday': self.employee.birthday,
            'telephone': self.employee.telephone,
            'online': self.employee.online_status
        }

        self.assertEqual(employee_info, self.employee.get_all_info())

    def test_str_method_links_resources(self):
        self.assertEqual(self.test_link.title, str(self.test_link))

    def test_get_info_method_links_resources(self):
        correct_meaning = {self.test_link.title: self.test_link.link}
        self.assertEqual(correct_meaning, self.test_link.get_info())


class TestCompanyModel(Settings):

    def setUp(self):
        self.test_department = test_models.Department.objects.create(
            company_id=self.company,
            title='test_title_1',
            supervisor=self.employee
        )
        self.test_position = test_models.Positions.objects.create(
            company_id=self.company,
            title='test_title_1',
        )
        self.test_company_event = test_models.CompanyEvent.objects.create(
            company=self.company,
            title='test_title_1',
            time_start=timezone.datetime(2024, 3, 10, 13, 17, 26, 134531, tzinfo=timezone.utc),
            time_end=timezone.datetime(2025, 3, 10, 13, 17, 26, 134531, tzinfo=timezone.utc)
        )

    def test_str_method_company(self):
        correct_meaning = f'{self.company.id}, {self.company.title}'
        self.assertEqual(correct_meaning, str(self.company))

    def test_get_absolute_url_method_company(self):
        correct_meaning = reverse('team:company', kwargs={'company_id': self.company.id})
        self.assertEqual(correct_meaning, self.company.get_absolute_url())

    def test_str_method_department(self):
        self.assertEqual(self.test_department.title, str(self.test_department))

    def test_get_absolute_url_method_department(self):
        correct_meaning = reverse('team:department', kwargs={
            'company_id': self.test_department.company_id.id,
            'department_id': self.test_department.id
        })
        self.assertEqual(correct_meaning, self.test_department.get_absolute_url())

    def test_str_method_position(self):
        self.assertEqual(self.test_position.title, str(self.test_position))

    def test_get_absolute_url_method_position(self):
        correct_meaning = reverse('team:position', kwargs={
            'company_id': self.test_position.company_id.id,
            'position_id': self.test_position.id
        })
        self.assertEqual(correct_meaning, self.test_position.get_absolute_url())

    def test_str_method_company_event(self):
        self.assertEqual(self.test_company_event.title, str(self.test_company_event))

    def test_save_method_company_event(self):
        with self.assertRaises(ValidationError):
            teste_company_event_2 = test_models.CompanyEvent.objects.create(
                company=self.company,
                title='test_title_2',
                time_start=timezone.datetime.now(),
                time_end=timezone.datetime.now() - timezone.timedelta(hours=1)
            )

        self.assertTrue(test_models.CompanyEvent.objects.filter(title='test_title_1').exists())


class TestProjectModel(Settings):

    def test_str_method_project(self):
        self.assertEqual(self.project.title, str(self.project))

    def test_get_absolute_url_method_project(self):
        correct_meaning = reverse('team:project', kwargs={
            'company_id': self.project.company_id.id,
            'project_id': self.project.id
        })
        self.assertEqual(correct_meaning, self.project.get_absolute_url())

    def test_get_default_task_status_method_project(self):
        correct_meaning = self.project._default_task_status
        self.assertEqual(correct_meaning, self.project.get_default_task_status)

    def test_set_default_task_status_method_project(self):
        with self.assertRaises(ValidationError):
            self.project.get_default_task_status = 'gibberish'

        with self.subTest():
            first_meaning = self.project.get_default_task_status
            self.project.get_default_task_status = list(self.project.task_status['status'])[-1]
            second_meaning = self.project.get_default_task_status
            self.assertTrue(first_meaning != second_meaning)

    def test_get_default_hand_over_task_status_method_project(self):
        correct_meaning = self.project._default_hand_over_task_status
        self.assertEqual(correct_meaning, self.project.get_default_hand_over_task_status)

    def test_set_default_hand_over_task_status_method_project(self):
        with self.assertRaises(ValidationError):
            self.project.get_default_hand_over_task_status = 'gibberish'

        with self.subTest():
            first_meaning = self.project.get_default_hand_over_task_status
            self.project.get_default_hand_over_task_status = list(self.project.task_status['status'])[-2]
            second_meaning = self.project.get_default_hand_over_task_status
            self.assertTrue(first_meaning != second_meaning)

    def test_update_task_status_method_project(self):
        with self.assertRaises(ValidationError):
            self.project.update_task_status(['test_status_1', 1])

        with self.subTest():
            new_status = ['test_status_1', 20]
            self.project.update_task_status(new_status)
            self.assertTrue(new_status[1] in self.project.task_status['status'].values())

    def test_delete_task_status_method_project(self):
        with self.assertRaises(ValidationError):
            self.project.delete_task_status(self.project.get_default_task_status)

        with self.assertRaises(ValidationError):
            self.project.delete_task_status(self.project.get_default_hand_over_task_status)\

        with self.assertRaises(ValidationError):
            self.project.delete_task_status('gibberish')

        with self.subTest():
            tasks_satus = self.project.task_status['status']
            test_delete_status = list(tasks_satus)[-1]
            self.project.delete_task_status(test_delete_status)

            self.assertTrue(test_delete_status not in tasks_satus)


class TestTaskModel(Settings):

    def setUp(self):
        self.test_subtask = test_models.Subtasks.objects.create(
            task_id=self.task,
            title='test_title_1',
        )

    def test_str_method_task(self):
        correct_meaning = self.task.title
        self.assertEqual(correct_meaning, str(self.task))

    def test_save_method(self):
        correct_meaning = self.task.project_id.get_default_task_status
        self.assertEqual(correct_meaning, self.task.task_status)

    def test_get_absolute_url_method_project(self):
        correct_meaning = reverse('team:task', kwargs={
            'company_id': self.task.project_id.company_id.id,
            'project_id': self.task.project_id.id,
            'task_id': self.task.id
        })
        self.assertEqual(correct_meaning, self.task.get_absolute_url())

    def test_str_method_task_dead_line(self):
        correct_meaning = self.task.title
        self.assertEqual(correct_meaning, str(self.task))

    def test_str_method_subtasks(self):
        correct_meaning = self.test_subtask.title
        self.assertEqual(correct_meaning, str(self.test_subtask))

    def test_get_absolute_url_method_subtasks(self):
        correct_meaning = reverse('team:subtask', kwargs={
            'company_id': self.test_subtask.task_id.project_id.company_id.id,
            'project_id': self.test_subtask.task_id.project_id.id,
            'task_id': self.test_subtask.task_id.id,
            'subtask_id': self.test_subtask.id
        })
        self.assertEqual(correct_meaning, self.test_subtask.get_absolute_url())
