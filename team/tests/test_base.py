from django.test import TestCase
from team import models as team_models
from QuickHub import settings
import tempfile, shutil


class Settings(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.employee = team_models.Employee.objects.create(username='test_username_1', name='test_user_1', password='test_password_1', email='test_email_1@gmail.com')
        cls.company = team_models.Company.objects.create(title='test_company_1', owner_id=cls.employee.id)
        cls.project = team_models.Project.objects.create(company_id=cls.company, title='test_title_1', project_creater=cls.employee.id)
        cls.task = team_models.Task.objects.create(project_id=cls.project, title='test_title_1')
        cls.employee.companies.add(cls.company)
        cls.employee.tasks.add(cls.task)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
