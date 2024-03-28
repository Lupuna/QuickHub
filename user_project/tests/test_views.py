from django.test import TestCase, Client
from django.urls import reverse
from django.db.models import Count

from team import models as team_models
from user_project import models as user_project_models



class TestViews(TestCase):
    fixtures = ['data.json']

    def setUp(self):
        self.user = team_models.Employee.objects.get(id=2)

        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.create_category_url = reverse('user_project:create_category')
        self.create_taskboard_url = reverse('user_project:create_taskboard')
        self.taskboard_url = reverse('user_project:taskboard')
        self.taskboard_edit_url = reverse('user_project:add_task', args=[1])
        # self.login_url = reverse('registration:login')

        self.taskboard_template = 'user_project/main_functionality/taskboard.html'
        self.creation_template = 'includes/creator.html'

    # /// ТЕСТЫ ДЛЯ АВТОРИЗОВАННОГО ПОЛЬЗОВАТЕЛЯ ///

    def test_create_category_GET(self):
        response = self.authorized_client.get(self.create_category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.creation_template)

    def test_create_taskboard_GET(self):
        response = self.authorized_client.get(self.create_taskboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.creation_template)

    def test_taskboard_list_GET(self):
        response = self.authorized_client.get(self.taskboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.taskboard_template)

    def test_edit_taskboard_GET(self):
        response = self.authorized_client.get(self.taskboard_edit_url)
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

        user_project_models.Category.objects.filter(**data).delete()
        count = user_project_models.Category.objects.filter(**data).count()
        
        self.assertEqual(count, 0)

        response = self.authorized_client.post(
            self.create_category_url, 
            data=data,
        )
        category = user_project_models.Category.objects.get(**data)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.taskboard_url)
        self.assertEquals(self.user, category.employee_id)
    
    # def test_create_taskboard_POST(self):
    #     category = user_project_models.Category.objects.create(
    #         title='TEST',
    #         employee_id=self.user,
    #     )

    #     task = team_models.Task.objects.create(
    #         title='test Task1',
    #         project_id=team_models.Project.objects.get(id=1)
    #     )
    #     task.executors.add(self.user)

    #     self.assertEqual(task.title, 'test Task1')
    #     self.assertEqual(category.title, 'TEST')

    #     response = self.authorized_client.post(
    #         self.create_taskboard_url,
    #         data={
    #             'category': 'TEST',
    #             'tasks': ['test Task1', ],
    #             'text': 'NOTES',
    #         },
    #         content_type='application/x-www-form-urlencoded'
    #     )

    #     taskboard = user_project_models.Taskboard.objects.filter(
    #         category_id=category,
    #         task_id=task,
    #     )

    #     self.assertEqual(taskboard.count(), 1)

    #     self.assertEqual(response.status_code, 302)
        # self.assertEqual(taskboard.title, 'TEST')

        # self.assertRedirects(response, self.taskboard_url)

    def test_correct_count_categories(self):
        response = self.authorized_client.get(self.taskboard_url)

        categories = self.user.categories.all()
        total = categories.count()
        count = len(response.context['categories'])

        self.assertEqual(count, total, f'Ожидалось {total} категорий. Отображено {count}.')
        self.assertQuerySetEqual(categories, response.context['categories'], ordered=False)

    def test_correct_count_tasks_in_categories(self):
        response = self.authorized_client.get(self.taskboard_url)

        categories = self.user.categories\
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

