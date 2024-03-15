from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user_project import views as user_project_views


class TestUrls(SimpleTestCase):

    def test_taskboard_url_is_resolve(self):
        url = reverse('user_project:taskboard')
        self.assertEqual(resolve(url).func.view_class, user_project_views.TaskboardListView)

    def test_create_category_url_is_resolve(self):
        url = reverse('user_project:create_category')
        self.assertEqual(resolve(url).func.view_class, user_project_views.CreateCategory)

    def test_create_taskboard_url_is_resolve(self):
        url = reverse('user_project:create_taskboard')
        self.assertEqual(resolve(url).func.view_class, user_project_views.CreateTaskboard)

    def test_add_task_url_is_resolve(self):
        url = reverse('user_project:add_task', args=[1])
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, user_project_views.CreateTaskboard)
