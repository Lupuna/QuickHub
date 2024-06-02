from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user_project_time import views as user_project_time_views


class TestUrls(SimpleTestCase):

    def test_taskboard_url_is_resolve(self):
        url = reverse('user_project_time:taskboard')
        self.assertEqual(resolve(url).func.view_class, user_project_time_views.DeadlineCategoriesListView)

    def test_create_category_slug_Overtimed_is_resolve(self):
        url = reverse('user_project_time:deadline_detail', args=['Overtimed'])
        self.assertEqual(resolve(url).func.view_class, user_project_time_views.DeadlineCategoryDetailView)
    
    def test_create_category_slug_Today_is_resolve(self):
        url = reverse('user_project_time:deadline_detail', args=['Today'])
        self.assertEqual(resolve(url).func.view_class, user_project_time_views.DeadlineCategoryDetailView)
    
    def test_create_category_slug_Tomorrow_is_resolve(self):
        url = reverse('user_project_time:deadline_detail', args=['Tomorrow'])
        self.assertEqual(resolve(url).func.view_class, user_project_time_views.DeadlineCategoryDetailView)
    
    def test_create_category_slug_Week_is_resolve(self):
        url = reverse('user_project_time:deadline_detail', args=['Week'])
        self.assertEqual(resolve(url).func.view_class, user_project_time_views.DeadlineCategoryDetailView)
    
    def test_create_category_slug_Month_is_resolve(self):
        url = reverse('user_project_time:deadline_detail', args=['Month'])
        self.assertEqual(resolve(url).func.view_class, user_project_time_views.DeadlineCategoryDetailView)
    
    def test_create_category_slug_Not_soon_is_resolve(self):
        url = reverse('user_project_time:deadline_detail', args=['Not_soon'])
        self.assertEqual(resolve(url).func.view_class, user_project_time_views.DeadlineCategoryDetailView)
    
    def test_create_category_slug_Permanent_is_resolve(self):
        url = reverse('user_project_time:deadline_detail', args=['Permanent'])
        self.assertEqual(resolve(url).func.view_class, user_project_time_views.DeadlineCategoryDetailView)

    

