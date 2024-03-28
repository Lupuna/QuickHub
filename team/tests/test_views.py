from .test_base import Settings
from django.test import Client, RequestFactory
from django.urls import reverse
from team import views as team_views


class TestEmployeeView(Settings):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_user_companies_list_view(self):
        url = reverse('team:companies')
        request = self.factory.get(url)
        request.user = self.employee
        with self.subTest():
            response = team_views.UserCompaniesListView.as_view()(request)
            self.assertEqual(200, response.status_code)

        with self.subTest():
            view = team_views.UserCompaniesListView()
            view.setup(request)
            correct_meaning = request.user.companies.all()
            self.assertQuerySetEqual(correct_meaning, view.get_queryset())

    # to do complete test for get_context_data()
    def test_user_project_list_view(self):
        url = reverse('team:projects')
        request = self.factory.get(url)
        request.user = self.employee
        with self.subTest():
            response = team_views.UserProjectsListView.as_view()(request)
            self.assertEqual(200, response.status_code)

        with self.subTest():
            view = team_views.UserProjectsListView()
            view.setup(request)
            tasks = request.user.tasks.select_related('project_id').all()
            correct_meaning = []
            for task in tasks:
                project = task.project_id
                if project not in correct_meaning:
                    correct_meaning.append(project)
            self.assertQuerySetEqual(correct_meaning, view.get_queryset())

    def test_user_profile_list_view(self):
        url = reverse('team:user_profile')
        request = self.factory.get(url)
        request.user = self.employee
        with self.subTest():
            response = team_views.UserProfileListView.as_view()(request)
            self.assertEqual(200, response.status_code)

        with self.subTest():
            view = team_views.UserProfileListView()
            view.setup(request)
            correct_meaning = request.user.companies.all()
            self.assertQuerySetEqual(correct_meaning, view.get_queryset())
