from django.test import SimpleTestCase
from user_project import forms as user_project_forms


# to do: add_test_taskboard_creation_from_no_data, add_test_taskboard_creation_from_valid_form


class TestForms(SimpleTestCase):

    def test_category_creation_from_valid_form(self):
        form = user_project_forms.CategoryCreationForm(data={
            'title': 'test_title',
            'project_personal_notes': 'test_project_personal_notes'
        })

        self.assertTrue(form.is_valid())

    def test_category_creation_from_no_data(self):
        form = user_project_forms.CategoryCreationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
