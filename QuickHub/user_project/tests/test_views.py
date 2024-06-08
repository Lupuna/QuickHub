import django.test
from django.test import Client
from django.urls import reverse
from django.db.models import Count

from team.tests.test_base import SettingsView
import team
from .. import models


class TestViews(SettingsView):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.guest_client = Client()

        cls.create_category_url = reverse('user_project:create_category')
        cls.create_taskboard_url = reverse('user_project:create_taskboard')
        cls.taskboard_url = reverse('user_project:taskboard')
        cls.login_url = reverse('q_registration:login')

        cls.taskboard_template = 'user_project/main_functionality/taskboard.html'
        cls.creation_template = 'includes/creator.html'

    def setUp(self) -> None:
        super().setUp()
        category = models.Category.objects.create(
            title="TEST",
            employee_id=self.employee
        )
        self.taskboard_edit_url = reverse('user_project:add_task', args=[category.id])

    # /// ТЕСТЫ ДЛЯ АВТОРИЗОВАННОГО ПОЛЬЗОВАТЕЛЯ ///

    def test_create_category_GET(self):
        response = self.auth_client.get(self.create_category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.creation_template)

    def test_create_taskboard_GET(self):
        response = self.auth_client.get(self.create_taskboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.creation_template)

    def test_taskboard_list_GET(self):
        response = self.auth_client.get(self.taskboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.taskboard_template)

    def test_edit_taskboard_GET(self):
        response = self.auth_client.get(self.taskboard_edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.creation_template)

    # /// ТЕСТЫ ДЛЯ НЕАВТОРИЗОВАННОГО ПОЛЬЗОВАТЕЛЯ ///

    def test_create_category_GET_quest(self):
        response = self.guest_client.get(self.create_category_url)
        self.assertEqual(response.status_code, 302)

    def test_create_taskboard_GET_guest(self):
        response = self.guest_client.get(self.create_taskboard_url)
        self.assertEqual(response.status_code, 302)

    def test_taskboard_list_GET_guest(self):
        response = self.guest_client.get(self.taskboard_url)
        self.assertEqual(response.status_code, 302)

    def test_edit_taskboard_GET_guest(self):
        response = self.guest_client.get(self.taskboard_edit_url)
        self.assertEqual(response.status_code, 302)

    # /// ТЕСТЫ ФУНКЦИОНАЛЬНОСТИ ///
        
    def test_create_category_POST(self):
        data = {
            'title': 'Тест',
            'project_personal_notes': 'Заметки',
        }

        models.Category.objects.filter(**data).delete()
        count = models.Category.objects.filter(**data).count()
        
        self.assertEqual(count, 0)

        response = self.auth_client.post(
            self.create_category_url, 
            data=data,
        )
        category = models.Category.objects.get(**data)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.taskboard_url)
        self.assertEquals(self.employee, category.employee_id)


    # def test_create_taskboard_POST(self):
    #     category = models.Category.objects.create(
    #         title='TEST',
    #         employee_id=self.employee,
    #     )
    #     self.assertEqual(category.title, 'TEST')
    #
    #     response = self.auth_client.post(
    #         self.create_taskboard_url,
    #         data={
    #             'category': 'TEST',
    #             'tasks': ['test_title_1', ],
    #             'text': 'NOTES',
    #         },
    #         # content_type='application/x-www-form-urlencoded'
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, self.creation_template)

        # taskboard = models.Taskboard.objects.filter(
        #     category_id=category,
        #     task_id=self.task,
        # )

        # self.assertEqual(taskboard.count(), 1)

        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(taskboard.title, 'TEST')
        #
        # self.assertRedirects(response, self.taskboard_url)

    def test_correct_count_categories(self):
        response = self.auth_client.get(self.taskboard_url)

        categories = self.employee.categories.all()
        total = categories.count()
        count = len(response.context['categories'])

        self.assertEqual(count, total, f'Ожидалось {total} категорий. Отображено {count}.')
        self.assertQuerySetEqual(categories, response.context['categories'], ordered=False)

    def test_correct_count_tasks_in_categories(self):
        response = self.auth_client.get(self.taskboard_url)

        categories = self.employee.categories\
            .prefetch_related('tasks')\
            .annotate(tasks_count=Count('tasks'))\
            .order_by('title')
        context_categories = sorted(response.context['categories'], key=lambda x: x.title)
        
        for category, context_category in zip(categories, context_categories):
            with self.subTest():
                total_tasks = category.tasks.count()
                context_count_tasks = context_category.tasks.count()
                
                self.assertEqual(total_tasks, context_count_tasks)

                self.assertQuerySetEqual(
                    category.tasks.all(), 
                    context_category.tasks.all(), 
                    ordered=False
                )

