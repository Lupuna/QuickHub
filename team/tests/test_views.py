from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from team import views as team_views
from team import models as team_models
from django.db.models import Count, Q


class TestEmployeeView(TestCase):
    fixtures = ['data.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.auth_client = Client()
        self.employee = team_models.Employee.objects.get(id=2)
        self.auth_client.force_login(self.employee)

    def test_user_companies_list_view(self):
        url = reverse('team:companies')
        template = 'team/main_functionality/list_views/user_companies.html'
        request = self.factory.get(url)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(200, response.status_code)
            self.assertTemplateUsed(response, template)

        with self.subTest('view functionality'):
            view = team_views.UserCompaniesListView()
            view.setup(request)
            correct_meaning = request.user.companies.all()
            self.assertQuerySetEqual(correct_meaning, view.get_queryset())

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)

    def test_user_projects_list_view(self):
        url = reverse('team:projects')
        template = 'team/main_functionality/list_views/user_projects.html'
        request = self.factory.get(url)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('view functionality'):
            view = team_views.UserProjectsListView()
            view.setup(request)
            tasks = request.user.tasks.select_related('project_id')
            projects_ids = tasks.values_list('project_id', flat=True)
            correct_meaning = team_models.Project.objects.filter(id__in=projects_ids).annotate(
                tasks_count=Count('tasks'),
                ready_count=Count('tasks', filter=Q(tasks__task_status='Ready'))
            )
            with self.assertNumQueries(2):
                self.assertQuerySetEqual(correct_meaning, view.get_queryset())

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)

    def test_user_profile_list_view(self):
        url = reverse('team:user_profile')
        template = 'team/main_functionality/list_views/user_profile.html'
        request = self.factory.get(url)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('view functionality'):
            view = team_views.UserProfileListView()
            view.setup(request)
            correct_meaning = request.user.companies.all()
            self.assertEqual(view.get_queryset(), correct_meaning)
