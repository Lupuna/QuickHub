from django.test import Client, RequestFactory, TestCase
from team import models as team_models
import user_project
import user_project_time
from QuickHub import settings
import tempfile, shutil


class Settings(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.employee = team_models.Employee.objects.create(username='test_username_1', name='test_user_1',
                                                           password='test_password_1', email='test_email_1@gmail.com')
        cls.company = team_models.Company.objects.create(title='test_company_1', owner_id=cls.employee.id)
        cls.project = team_models.Project.objects.create(company_id=cls.company, title='test_title_1',
                                                         project_creater=cls.employee.id)
        cls.task = team_models.Task.objects.create(project_id=cls.project, title='test_title_1')
        cls.employee.companies.add(cls.company)
        cls.employee.tasks.add(cls.task)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)


class SettingsView(Settings):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.factory = RequestFactory()
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.employee)

class SettingsPermissions(SettingsView):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.other_employee = team_models.Employee.objects.create(
            username='test_username_2',
            name='test_user_2',
            password='test_password_2',
            email='test_email_2@gmail.com'
        )

        cls.forbidden_company = team_models.Company.objects.create(
            title="test_company_2",
            owner_id=cls.other_employee.id,
        )

        cls.forbidden_project_other_company = team_models.Project.objects.create(
            company_id=cls.forbidden_company,
            title="test_project_2",
            project_creater=cls.other_employee.id,
        )
        cls.forbidden_project_user_company = team_models.Project.objects.create(
            company_id=cls.company,
            title="test_project_3",
            project_creater=4,
        )

        cls.task_from_forbidden_project = team_models.Task.objects.create(
            project_id=cls.forbidden_project_other_company,
            title="test_task_2"
        )
        cls.task_from_forbidden_project_user_company = team_models.Task.objects.create(
            project_id=cls.forbidden_project_user_company,
            title="test_task_3"
        )
        cls.task_user_is_not_executor = team_models.Task.objects.create(
            project_id=cls.project,
            title="test_task_3"
        )
        cls.task_user_is_not_executor.executors.add(cls.other_employee)

        cls.forbidden_subtask = team_models.Subtasks.objects.create(
            task_id=cls.task_from_forbidden_project,
            title="test_subtask_1"
        )
        cls.other_employee.companies.add(cls.forbidden_company)
        cls.other_employee.tasks.add(cls.task_from_forbidden_project, cls.task_user_is_not_executor)


class SetUpServicesMixin(TestCase):
    def setUp(self):
        super().setUp()
        self.executor1 = self._create_executor(id=1)
        self.executor2 = self._create_executor(id=2)
        self.executor3 = self._create_executor(id=3)

        self._create_category(self.executor1)
        self._create_category(self.executor2)
        self._create_category(self.executor3)

        self._create_time_categories(self.executor1)
        self._create_time_categories(self.executor2)
        self._create_time_categories(self.executor3)

        self.company.employees.add(self.executor1, self.executor2, self.executor3)
        self.task.executors.add(self.executor1, self.executor2, self.executor3)

        self.executors = self.task.executors.all()

    @classmethod
    def _create_executor(cls, id: int):
        return team_models.Employee.objects.create(
            username=f'test_executor_{id}',
            name=f'test_executor_{id}',
            password=f'test_password_{id}',
            email=f'email_{id}@gmail.com'
        )

    @classmethod
    def _create_category(cls, user):
        return user_project.models.Category.objects.create(
            title="Мои задачи",
            employee_id=user
        )

    @classmethod
    def _create_time_categories(cls, user: team_models.Employee):
        for status in user_project_time.models.UserTimeCategory.Status:
            user_project_time.models.UserTimeCategory.objects.create(
                employee_id=user.id,
                status=status
            )
