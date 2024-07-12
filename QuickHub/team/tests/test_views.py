from django.urls import reverse
from team import views as team_views
from team import models as team_models
from .test_base import SettingsView
from django.db.models import Count, Q


class TestEmployeeView(SettingsView):

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
                self.assertQuerySetEqual(correct_meaning, view.get_queryset(), ordered=False)

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
            self.assertQuerySetEqual(correct_meaning, view.get_queryset())

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)


class TestCompanyView(SettingsView):

    def setUp(self):
        super().setUp()
        self.department = team_models.Department.objects.create(
            company_id=self.company,
            title='test_title_1',
            supervisor=self.employee
        )

    def test_create_company(self):
        url = reverse('team:create_company')
        template = 'includes/creator.html'
        request = self.factory.get(url)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)

    def test_create_position(self):
        url = reverse('team:create_position', args=[self.company.id])
        template = 'includes/creator.html'
        request = self.factory.get(url)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)

    def test_create_company_event(self):
        url = reverse('team:create_company_event', args=[self.company.id])
        template = 'includes/creator.html'
        request = self.factory.get(url)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('view functionality'):
            view = team_views.CreateCompanyEvent()
            view.setup(request, company=self.company)
            self.assertEqual(view.get_form_kwargs()['company_id'], self.company)

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)

    def test_create_department(self):
        url = reverse('team:create_department', args=[self.company.id])
        template = 'includes/creator.html'
        request = self.factory.get(url)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('view functionality'):
            view = team_views.CreateCompanyEvent()
            view.setup(request, company=self.company)
            self.assertEqual(view.get_form_kwargs()['company_id'], self.company)

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)

    def test_check_employee(self):
        url = reverse('team:check_employee', args=[self.company.id])
        template = 'team/main_functionality/list_views/company_employees.html'
        request = self.factory.get(url)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('view functionality'):
            view = team_views.CheckEmployee()
            view.setup(request, company=self.company, company_id=self.company.id)
            with self.assertNumQueries(3):
                view.get_queryset()

            with self.subTest('get_success'):
                correct_meaning = reverse('team:check_employee', kwargs={'company_id': self.company.id})
                self.assertEqual(view.get_success_url(), correct_meaning)

            with self.subTest('get_form_kwargs'):
                correct_meaning = 'name'
                self.assertEqual(view.get_form_kwargs()['sort_param'], correct_meaning)

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)

    def test_choice_parameters(self):
        url = reverse('team:choice_parameters', args=[self.company.id])
        template = 'team/main_functionality/choice_parameters.html'
        request = self.factory.get(url)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('view functionality'):
            view = team_views.ChoiceParameters()
            view.setup(request, company_id=self.company.id)
            correct_meaning = reverse('team:check_employee', kwargs={'company_id': self.company.id})
            self.assertEqual(correct_meaning, view.get_success_url())

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)

    def test_company_detail_view(self):
        url = reverse('team:company', args=[self.company.id])
        template = 'team/main_functionality/detail_views/company.html'
        request = self.factory.get(url, company_id=self.company.id)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('view functionality'):
            view = team_views.CompanyDetailView()
            view.setup(request, company=self.company)
            with self.subTest('test get_object'):
                correct_meaning = self.company
                self.assertEqual(correct_meaning, view.get_object())

            with self.subTest('test get_context_data'):
                correct_meaning = view.get_object().departments.select_related('supervisor').prefetch_related('childs') \
                    .filter(parent_id=None)
                with self.assertNumQueries(2):
                    self.assertQuerySetEqual(correct_meaning, response.context['roots'])

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)

    def test_positions_list_view(self):
        url = reverse('team:positions_list', args=[self.company.id])
        template = 'team/main_functionality/list_views/positions.html'
        request = self.factory.get(url, company_id=self.company.id)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('view functionality'):
            view = team_views.PositionsListView()
            view.setup(request, company=self.company)
            correct_meaning = self.company.positions.all()
            self.assertQuerySetEqual(correct_meaning, view.get_queryset(), ordered=False)

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)

    def test_department_detail_view(self):
        url = reverse('team:department', args=[self.company.id, self.department.id])
        template = 'team/main_functionality/detail_views/department.html'
        request = self.factory.get(url, company_id=self.company.id, department_id=self.department.id)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('view functionality'):
            view = team_views.DepartmentDetailView()
            view.setup(request, company=self.company, department_id=self.department.id)
            correct_meaning = team_models.Department.objects.select_related('supervisor').get(id=self.department.id)
            with self.assertNumQueries(1):
                self.assertEqual(correct_meaning, view.get_object())

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)

    def test_departments_list_view(self):
        url = reverse('team:departments_list', args=[self.company.id])
        template = 'team/main_functionality/list_views/departments.html'
        request = self.factory.get(url, company=self.company)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('view functionality'):
            view = team_views.DepartmentsListView()
            view.setup(request, company=self.company)
            correct_meaning = self.company.departments.all()
            with self.assertNumQueries(2):
                self.assertQuerySetEqual(correct_meaning, view.get_queryset())

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)


class TestProjectView(SettingsView):

    def test_positions_list_view(self):
        url = reverse('team:positions_list', args=[self.company.id])
        template = 'team/main_functionality/list_views/positions.html'
        request = self.factory.get(url, company=self.company)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('view functionality'):
            view = team_views.PositionsListView()
            view.setup(request, company=self.company)
            correct_meaning = self.company.positions.all()
            with self.assertNumQueries(2):
                self.assertQuerySetEqual(correct_meaning, view.get_queryset(), ordered=False)

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)


class TestTaskView(SettingsView):

    def test_create_task_view(self):
        url = reverse('team:create_task', args=[self.company.id, self.project.id])
        template = 'includes/creator.html'
        request = self.factory.get(url, company=self.company, project=self.project)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('view functionality'):
            view = team_views.CreateTask()
            view.setup(request, company=self.company, project=self.project)
            with self.subTest('test get_form_kwargs'):
                self.assertEqual(view.get_form_kwargs()['company_id'], self.company)
                self.assertEqual(view.get_form_kwargs()['project_id'], self.project)

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)

    def test_task_detail__view(self):
        url = reverse('team:task', args=[self.company.id, self.project.id, self.task.id])
        template = 'team/main_functionality/detail_views/task.html'
        request = self.factory.get(url, company=self.company, project=self.project, task=self.task)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('view functionality'):
            view = team_views.TaskDetailView()
            view.setup(request, company=self.company, project=self.project, task=self.task)
            with self.subTest('test get_object'):
                correct_meaning = self.task
                self.assertEqual(correct_meaning, view.get_object())

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)

    def test_task_update__view(self):
        url = reverse('team:task_update', args=[self.company.id, self.project.id, self.task.id])
        template = 'team/main_functionality/update_views/task.html'
        request = self.factory.get(url, company=self.company, project=self.project, task=self.task)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('view functionality'):
            view = team_views.TaskUpdateView()
            view.setup(request, company=self.company, project=self.project, task=self.task)
            with self.subTest('test get_object'):
                correct_meaning = self.task
                self.assertEqual(correct_meaning, view.get_object())

            with self.subTest('test get_initial'):
                correct_meaning = {
                    'title': self.task.title,
                    'text': self.task.text,
                    'time_start': self.task.time_start,
                    'time_end': self.task.time_end,
                    'parent_id': self.task.parent_id,
                }
                initial = view.get_initial()
                self.assertQuerySetEqual(
                    team_models.Employee.objects.filter(email__in=self.task.json_with_employee_info.get('responsible', [])),
                    initial.pop('responsible')
                )
                self.assertQuerySetEqual(
                    team_models.Employee.objects.filter(email__in=self.task.json_with_employee_info.get('executor', [])),
                    initial.pop('executor')
                )
                self.assertEqual(correct_meaning, initial)

            with self.subTest('test get_form_kwargs'):
                kwargs = view.get_form_kwargs()
                self.assertEqual(kwargs['company_id'], self.company)
                self.assertEqual(kwargs['project_id'], self.project)
                self.assertEqual(None, kwargs.get('instance'))

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)

    def test_create_subtask_view(self):
        url = reverse('team:create_subtask', args=[self.company.id, self.project.id, self.task.id])
        template = 'includes/creator.html'
        request = self.factory.get(url, company=self.company, project=self.project, task=self.task)
        request.user = self.employee
        with self.subTest('auth user, GET'):
            response = self.auth_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

        with self.subTest('view functionality'):
            view = team_views.CreateSubtask()
            view.setup(request, company=self.company, project=self.project, task=self.task)
            with self.subTest('test get_form_kwargs'):
                kwargs = view.get_form_kwargs()
                self.assertEqual(kwargs['company_id'], self.company)

        with self.subTest('not auth user POST'):
            response = self.client.get(url)
            self.assertEqual(302, response.status_code)
