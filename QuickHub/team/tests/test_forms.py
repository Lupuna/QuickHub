from .test_base import Settings
from django.utils import timezone
from team import (forms as team_forms, models as team_models)


class TestCompanyForm(Settings):

    def test_company_creation_form(self):
        with self.subTest('valid data'):
            data = {
                'title': 'Test title'
            }
            form = team_forms.CompanyCreationForm(data=data)
            self.assertTrue(form.is_valid())

        with self.subTest('no valid data'):
            data = {}
            form = team_forms.CompanyCreationForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertEqual(len(form.errors), 1)

    def test_choice_employee_parameters_form(self):
        with self.subTest('valid data'):
            data = {
                'image': True,
                'name': False,
                'email': True,
                'telephone': True,
                'position_title': True,
                'department': True,
                'vk': True
            }
            form = team_forms.ChoiceEmployeeParametersForm(data=data)
            self.assertTrue(form.is_valid())

    def test_choice_sort_parameters_form(self):
        with self.subTest('valid data'):
            data = {
                'sorted_fields': 'name'
            }
            form = team_forms.ChoiceEmployeeParametersForm(data=data)
            self.assertTrue(form.is_valid())

    def test_department_creation_form(self):
        with self.subTest('valid data'):
            queryset = self.company.employees.distinct()
            data = {
                'title': 'Test title',
                'supervisor': queryset[0],
                'employees': queryset
            }

            form = team_forms.DepartmentCreationForm(data=data, company_id=self.company)
            with self.subTest('test queryset'):
                correct_meaning = [
                    queryset,
                    queryset,
                    team_models.Department.objects.filter(company_id=self.company)
                ]
                with self.assertNumQueries(5):
                    self.assertQuerySetEqual(correct_meaning[0], form.fields['supervisor'].queryset)
                    self.assertQuerySetEqual(correct_meaning[1], form.fields['employees'].queryset)
                    self.assertQuerySetEqual(correct_meaning[2], form.fields['parent'].queryset)
            self.assertTrue(form.is_valid())

        with self.subTest('no valid data'):
            data = {}
            form = team_forms.DepartmentCreationForm(data=data, company_id=self.company)
            self.assertFalse(form.is_valid())
            self.assertEqual(len(form.errors), 3)

    def test_position_creation_form(self):
        with self.subTest('valid data'):
            data = {
                'title': 'Test title',
                'text': 'test text',
                'weight': 1
            }

            form = team_forms.PositionCreationForm(data=data)
            self.assertTrue(form.is_valid())

        with self.subTest('no valid data'):
            data = {}
            form = team_forms.PositionCreationForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertEqual(len(form.errors), 2)

    def test_company_event_creation_form(self):
        with self.subTest('valid data'):
            data = {
                'title': 'Test title',
                'time_start': timezone.now(),
                'time_end': timezone.now() + timezone.timedelta(days=30)
            }

            form = team_forms.CompanyEventCreationForm(data=data, company_id=self.company)
            with self.subTest('test queryset'):
                correct_meaning = [
                    self.company.employees.distinct(),
                ]
                with self.assertNumQueries(2):
                    self.assertQuerySetEqual(correct_meaning[0], form.fields['present_employees'].queryset)
            self.assertTrue(form.is_valid())

        with self.subTest('no valid data'):
            data = {
                    'time_start': timezone.now() + timezone.timedelta(days=30),
                    'time_end': timezone.now()
            }
            form = team_forms.CompanyEventCreationForm(data=data, company_id=self.company)
            self.assertFalse(form.is_valid())
            self.assertEqual(len(form.errors), 2)


class TestProjectForm(Settings):

    def test_project_creation_form(self):
        with self.subTest('valid data'):
            data = {
                'title': 'Test title',
                'view_counter': 1
            }

            form = team_forms.ProjectCreationForm(data=data)
            self.assertTrue(form.is_valid())

        with self.subTest('no valid data'):
            data = {}
            form = team_forms.ProjectCreationForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertEqual(len(form.errors), 2)


class TestTaskForm(Settings):

    def test_task_creation_form(self):
        with self.subTest('valid data'):
            queryset = self.company.employees.only('email')
            data = {
                'title': 'Test title',
                'responsible': queryset,
            }

            form = team_forms.TaskCreationForm(data=data, company_id=self.company, project_id=self.project)
            with self.subTest('test queryset'):
                correct_meaning = [
                    queryset,
                    queryset,
                    self.project.tasks.only('id', 'title')
                ]
                with self.assertNumQueries(7):
                    self.assertQuerySetEqual(correct_meaning[0], form.fields['responsible'].queryset)
                    self.assertQuerySetEqual(correct_meaning[1], form.fields['executor'].queryset)
                    self.assertQuerySetEqual(correct_meaning[2], form.fields['parent_id'].queryset)
            self.assertTrue(form.is_valid())

        with self.subTest('no valid data'):
            data = {
                'time_start': timezone.now() + timezone.timedelta(days=30),
                'time_end': timezone.now()
            }
            form = team_forms.TaskCreationForm(data=data, company_id=self.company, project_id=self.project)
            self.assertFalse(form.is_valid())
            self.assertEqual(len(form.errors), 3)

    def test_subtask_creation_form(self):
        with self.subTest('valid data'):
            queryset = self.company.employees.distinct()
            data = {
                'title': 'Test title',
                'responsible': queryset,
            }
            form = team_forms.SubtaskCreationForm(data=data, company_id=self.company)
            with self.subTest('test queryset'):
                correct_meaning = [
                    queryset,
                    queryset
                ]
                with self.assertNumQueries(3):
                    self.assertQuerySetEqual(correct_meaning[0], form.fields['responsible'].queryset)
                    self.assertQuerySetEqual(correct_meaning[1], form.fields['executor'].queryset)
            self.assertTrue(form.is_valid())

        with self.subTest('no valid data'):
            data = {}
            form = team_forms.SubtaskCreationForm(data=data, company_id=self.company)
            self.assertFalse(form.is_valid())
            self.assertEqual(len(form.errors), 2)
