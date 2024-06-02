from django.urls import reverse

from team import models
from .test_base import SettingsView


class TestCompanyAccessMixin(SettingsView):

    def setUp(self):
        super().setUp()
        self.forbidden_company = models.Company.objects.get(id=1)

    def test_correct_company(self):
        url = reverse('team:create_position', args=[self.company.id])
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_forbidden_company(self):
        url = reverse('team:create_position', args=[self.forbidden_company.id])
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_forbidden_company_correct_project(self):
        url = reverse('team:project', args=[
                      self.forbidden_company.id, self.project.id])
        request = self.factory.get(
            url,
            company_id=self.forbidden_company.id,
            project_id=self.project.id
        )
        request.user = self.employee
        response = self.auth_client.get(url)

        with self.subTest('correct project detail'):
            pass

        self.assertEqual(response.status_code, 200)


class TestProjectAccessMixin(SettingsView):

    def setUp(self):
        super().setUp()
        self.forbidden_project_other_company = models.Project.objects.get(id=4)
        self.forbidden_project_user_company = models.Project.objects.get(
            id=111)

    def test_correct_project(self):
        url = reverse('team:project', args=[self.company.id, self.project.id])
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)

        with self.subTest('correct project detail'):
            pass

    def test_forbidden_project_other_company(self):
        url = reverse('team:project', args=[
            self.company.id,
            self.forbidden_project_other_company.id,
        ])
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_forbidden_project_user_company(self):
        url = reverse('team:project', args=[
            self.company.id,
            self.forbidden_project_user_company.id,
        ])
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 403)


class TestTaskAccessMixin(SettingsView):

    def setUp(self):
        super().setUp()

        self.forbidden_project = models.Project.objects.get(id=111)

        self.task_user_is_not_executor = models.Task.objects.get(id=167)
        self.task_forbidden_project = models.Task.objects.filter(
            project_id__id=111).first()

    def test_correct_task(self):
        url = reverse('team:task', args=[
            self.company.id,
            self.project.id,
            self.task.id
        ])
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_task_from_forbidden_project(self):
        url = reverse('team:task', args=[
            self.company.id,
            self.forbidden_project.id,
            self.task_forbidden_project.id
        ])
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_task_user_is_not_executor(self):
        url = reverse('team:task', args=[
            self.company.id,
            self.project.id,
            self.task_user_is_not_executor.id
        ])
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, 200)
