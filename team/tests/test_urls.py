from django.test import SimpleTestCase
from django.urls import resolve, reverse
from team import views as team_views


class TestUrls(SimpleTestCase):

    def test_create_company_url_is_resolve(self):
        url = reverse('team:create_company')
        self.assertEqual(resolve(url).func.view_class, team_views.CreateCompany)

    def test_create_project_url_is_resolve(self):
        url = reverse('team:create_project', args=[1])
        self.assertEqual(resolve(url).func.view_class, team_views.CreateProject)

    def test_create_task_url_is_resolve(self):
        url = reverse('team:create_task', args=[1, 1])
        self.assertEqual(resolve(url).func.view_class, team_views.CreateTask)

    def test_create_department_url_is_resolve(self):
        url = reverse('team:create_department', args=[1])
        self.assertEqual(resolve(url).func.view_class, team_views.CreateDepartment)

    def test_create_subtask_url_is_resolve(self):
        url = reverse('team:create_subtask', args=[1, 1, 1])
        self.assertEqual(resolve(url).func.view_class, team_views.CreateSubtask)

    def test_create_position_url_is_resolve(self):
        url = reverse('team:create_position', args=[1])
        self.assertEqual(resolve(url).func.view_class, team_views.CreatePosition)

    def test_create_company_event_url_is_resolve(self):
        url = reverse('team:create_company_event', args=[1])
        self.assertEqual(resolve(url).func.view_class, team_views.CreateCompanyEvent)

    def test_check_employee_event_url_is_resolve(self):
        url = reverse('team:check_employee', args=[1])
        self.assertEqual(resolve(url).func.view_class, team_views.CheckEmployee)

    def test_choice_parameters_event_url_is_resolve(self):
        url = reverse('team:choice_parameters', args=[1])
        self.assertEqual(resolve(url).func.view_class, team_views.ChoiceParameters)

    def test_user_profile_event_url_is_resolve(self):
        url = reverse('team:user_profile')
        self.assertEqual(resolve(url).func.view_class, team_views.UserProfileListView)

    def test_company_url_is_resolve(self):
        url = reverse('team:company', args=[1])
        self.assertEqual(resolve(url).func.view_class, team_views.CompanyDetailView)

    def test_project_url_is_resolve(self):
        url = reverse('team:project', args=[1, 1])
        self.assertEqual(resolve(url).func.view_class, team_views.ProjectDetailView)

    def test_department_url_is_resolve(self):
        url = reverse('team:department', args=[1, 1])
        self.assertEqual(resolve(url).func.view_class, team_views.DepartmentDetailView)

    def test_task_url_is_resolve(self):
        url = reverse('team:task', args=[1, 1, 1])
        self.assertEqual(resolve(url).func.view_class, team_views.TaskDetailView)

    def test_subtask_url_is_resolve(self):
        url = reverse('team:subtask', args=[1, 1, 1, 1])
        self.assertEqual(resolve(url).func.view_class, team_views.SubtaskDetailView)

    def test_projects_list_url_is_resolve(self):
        url = reverse('team:projects_list', args=[1])
        self.assertEqual(resolve(url).func.view_class, team_views.ProjectsListView)

    def test_positions_list_url_is_resolve(self):
        url = reverse('team:positions_list', args=[1])
        self.assertEqual(resolve(url).func.view_class, team_views.PositionsListView)

    def test_departments_list_url_is_resolve(self):
        url = reverse('team:departments_list', args=[1])
        self.assertEqual(resolve(url).func.view_class, team_views.DepartmentsListView)

    def test_companies_url_is_resolve(self):
        url = reverse('team:companies')
        self.assertEqual(resolve(url).func.view_class, team_views.UserCompaniesListView)

    def test_projects_url_is_resolve(self):
        url = reverse('team:projects')
        self.assertEqual(resolve(url).func.view_class, team_views.UserProjectsListView)

    def test_update_task_url_is_resolve(self):
        url = reverse('team:task_update', args=[1, 1, 1])
        self.assertEqual(resolve(url).func.view_class, team_views.TaskUpdateView)

    def test_update_user_profile_url_is_resolve(self):
        url = reverse('team:update_user_profile', args=[1])
        self.assertEqual(resolve(url).func.view_class, team_views.UpdateUserProfile)

    def test_change_password_url_is_resolve(self):
        url = reverse('team:change_password')
        self.assertEqual(resolve(url).func.view_class, team_views.UserPasswordChangeView)

    def test_position_url_is_resolve(self):
        url = reverse('team:position', args=[1, 1])
        self.assertEqual(resolve(url).func.view_class, team_views.PositionDetailView)
