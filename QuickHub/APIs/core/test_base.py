from django.test import Client
from rest_framework.test import APITestCase

from team import models as team_models
from user_project import models as taskboards_models
from user_project_time import models as deadline_models


class UserTools:
    """Методы для создания тестовых данных для пользователя"""

    prefix = "api_test"

    @classmethod
    def create_user(cls, id: int) -> team_models.Employee:
        """Создание пользователя со всеми связанными с ним категориями"""

        user = cls._create_user(id)
        cls._create_user_category(user)

        for status in deadline_models.UserTimeCategory.Status:
            cls._create_user_deadlines_category(user=user, status=status)
        return user

    @classmethod
    def _create_user(cls, id: int) -> team_models.Employee:
        return team_models.Employee.objects.create(
            username=f"{cls.prefix}_user_{id}",
            name=f"{cls.prefix}_user_{id}",
            password=f"{cls.prefix}_password_{id}",
            email=f"{cls.prefix}_user_{id}@mail.ru",
        )

    @classmethod
    def _create_user_category(cls, user: team_models.Employee) -> taskboards_models.Category:
        return taskboards_models.Category.objects.create(
            title=f"{cls.prefix}_category_{user.name}",
            employee_id=user,
        )

    @classmethod
    def _create_user_deadlines_category(
        cls,
        user: team_models.Employee,
        status: deadline_models.UserTimeCategory.Status
    ) -> deadline_models.UserTimeCategory:
        """Создание категории срочности задач status для пользователя"""
        return deadline_models.UserTimeCategory.objects.create(
           employee=user,
           status=status
        )


class CompanyTools:
    """Методы для создания тестовых данных для компаний, отделов, проектов и задач"""

    prefix = "api_test"

    @classmethod
    def create_company(cls, id: int, owner: team_models.Employee) -> team_models.Company:
        return team_models.Company.objects.create(
            title=f"{cls.prefix}_company_{id}",
            owner_id=owner.id
        )

    @classmethod
    def create_department(
        cls,
        id: int,
        company: team_models.Company,
        supervisor: team_models.Employee,
    ) -> team_models.Department:
        """Создание отдела для компании"""
        return team_models.Department.objects.create(
            company_id=company,
            supervisor=supervisor,
            title=f"{cls.prefix}_department_{id}"
        )

    @classmethod
    def create_project(cls, id: int, company: team_models.Company) -> team_models.Project:
        return team_models.Project.objects.create(
            title=f"{cls.prefix}_project_{id}",
            company_id=company,
            project_creater=1,
            view_counter=team_models.Project.DisplayTypes.PARTIAL,
        )

    @classmethod
    def create_task(cls, id: int, project: team_models.Project) -> team_models.Task:
        return team_models.Task.objects.create(
            title=f"{cls.prefix}_task_{id}",
            text=f"{cls.prefix}_task_{id}_text",
            project_id=project,
        )

    @classmethod
    def create_subtask(cls, id: int, task: team_models.Task) -> team_models.Subtasks:
        return team_models.Subtasks.objects.create(
            title=f"{cls.prefix}_subtask_{id}",
            task_id=task,
        )


class APISettings(UserTools, CompanyTools, APITestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = cls.create_user(id=1)

        cls.company = cls.create_company(id=1, owner=cls.user)
        cls.user.companies.add(cls.company)

        cls.department = cls.create_department(id=1, supervisor=cls.user, company=cls.company)

        cls.project = cls.create_project(id=1, company=cls.company)

        cls.task = cls.create_task(id=1, project=cls.project)
        cls.task.executors.add(cls.user)

        cls.subtask = cls.create_subtask(id=1, task=cls.task)

        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.company.delete()
        super().tearDownClass()
