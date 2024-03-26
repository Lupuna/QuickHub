from django.test import TestCase, Client
from django.urls import reverse

from team.models import Employee
from user_project_time.models import UserTimeCategory


class TestViews(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.user = Employee.objects.get(id=1)
        self.authorized_client.force_login(self.user)

        self.taskboard_url = reverse('user_project_time:taskboard')
        self.category_url = {
            'Overtimed': reverse('user_project_time:deadline_detail', args=['Overtimed']),
            'Today': reverse('user_project_time:deadline_detail', args=['Today']),
            'Tomorrow': reverse('user_project_time:deadline_detail', args=['Tomorrow']),
            'Week': reverse('user_project_time:deadline_detail', args=['Week']),
            'Month': reverse('user_project_time:deadline_detail', args=['Month']),
            'Not_soon': reverse('user_project_time:deadline_detail', args=['Not_soon']),
            'Permanent': reverse('user_project_time:deadline_detail', args=['Permanent']),
        }
        self.login_url = reverse('registration:login')

        self.list_template = 'user_project_time/main_functionality/deadline_taskboard.html'
        self.detail_tempalte = 'user_project_time/main_functionality/detail_view.html'

    # /// ТЕСТЫ ДЛЯ АВТОРИЗОВАННОГО ПОЛЬЗОВАТЕЛЯ ///

    def test_deadline_categories_list_GET(self):
        response = self.authorized_client.get(self.taskboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.list_template)

    def test_deadline_category_OVERTIMED_detail_GET(self):
        response = self.authorized_client.get(self.category_url['Overtimed'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.detail_tempalte)
        
    def test_deadline_category_TODAY_detail_GET(self):
        response = self.authorized_client.get(self.category_url['Today'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.detail_tempalte)

    def test_deadline_category_TOMORROW_detail_GET(self):
        response = self.authorized_client.get(self.category_url['Tomorrow'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.detail_tempalte)

    def test_deadline_category_WEEK_detail_GET(self):
        response = self.authorized_client.get(self.category_url['Week'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.detail_tempalte)

    def test_deadline_category_MONTH_detail_GET(self):
        response = self.authorized_client.get(self.category_url['Month'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.detail_tempalte)

    def test_deadline_category_NOT_SOON_detail_GET(self):
        response = self.authorized_client.get(self.category_url['Not_soon'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.detail_tempalte)

    def test_deadline_category_PERMANTENT_detail_GET(self):
        response = self.authorized_client.get(self.category_url['Permanent'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.detail_tempalte)

    # /// ТЕСТЫ ДЛЯ НЕАВТОРИЗОВАННОГО ПОЛЬЗОВАТЕЛЯ ///

    def test_deadline_categories_list_GET_guest(self):
        response = self.guest_client.get(self.taskboard_url)
        self.assertEqual(response.status_code, 302)

    def test_deadline_category_OVERTIMED_detail_GET_guest(self):
        response = self.guest_client.get(self.category_url['Overtimed'])
        self.assertEqual(response.status_code, 302)
        
    def test_deadline_category_TODAY_detail_GET_guest(self):
        response = self.guest_client.get(self.category_url['Today'])
        self.assertEqual(response.status_code, 302)

    def test_deadline_category_TOMORROW_detail_GET_guest(self):
        response = self.guest_client.get(self.category_url['Tomorrow'])
        self.assertEqual(response.status_code, 302)

    def test_deadline_category_WEEK_detail_GET_guest(self):
        response = self.guest_client.get(self.category_url['Week'])
        self.assertEqual(response.status_code, 302)

    def test_deadline_category_MONTH_detail_GET_guest(self):
        response = self.guest_client.get(self.category_url['Month'])
        self.assertEqual(response.status_code, 302)

    def test_deadline_category_NOT_SOON_detail_GET_guest(self):
        response = self.guest_client.get(self.category_url['Not_soon'])
        self.assertEqual(response.status_code, 302)

    def test_deadline_category_PERMANTENT_detail_GET_guest(self):
        response = self.guest_client.get(self.category_url['Permanent'])
        self.assertEqual(response.status_code, 302)

    # /// ПРОВЕРКА ФУНКЦИОНАЛЬНОСТИ ///

    def test_correct_page_context(self):
        '''Проверка количества отображаемых категорий'''
        response = self.authorized_client.get(self.taskboard_url)
        
        count = len(response.context['time_categories'])
        needed_count = len(UserTimeCategory.Status)
        error_name = (f'Отображается {count } категорий',
                      f'Должно отображаться {needed_count} категорий')
        
        self.assertEqual(count, needed_count, error_name)