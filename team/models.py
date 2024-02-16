from django.contrib.auth.models import AbstractUser
from django.db import models
from . import utils


class Employee(AbstractUser):
    name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    telephone = models.CharField(max_length=40, blank=True, null=True)
    json_with_settings_info = models.JSONField(blank=True, default=dict)
    image = models.ImageField(upload_to='images/%Y/%m/%d/%H/', blank=True)
    
    tasks = models.ManyToManyField('Task', blank=True, related_name='executors')
    positions = models.ManyToManyField('Positions', through='EmployeeCompany', related_name='employees')
    departments = models.ManyToManyField('Department', through='EmployeeCompany', related_name='employees')
    companies = models.ManyToManyField('Company', through='EmployeeCompany', related_name='employees')

    def get_all_info(self):
        information = {
            'image': self.image,
            'name': self.name,
            'email': self.email,
            'city': self.city,
            'birthday': self.birthday,
            'telephone': self.telephone,
        }
        return information

    class Meta:
        ordering = ['username']
        unique_together = ['password', 'username']

    def __str__(self):
        return self.email


class LinksResources(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=200)
    link = models.URLField(max_length=200)

    def get_info(self):
        return {self.title: self.link}

    class Meta:
        order_with_respect_to = 'employee_id'


class Company(models.Model):
    title = models.CharField(max_length=250)
    owner_id = models.IntegerField(
        help_text='Тут будет храниться id создателя компании(т. е. того человека, который будет платить)')
    # json_with_department_info = models.JSONField(blank=True, default=dict)
    # json_with_settings_info = models.JSONField(blank=True, default=dict)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.owner_id}, {self.title}'


class Department(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='childs')
    title = models.CharField(max_length=40, unique=True)
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        ordering = ['company_id', 'title']
        unique_together = ['company_id', 'title']

    def __str__(self):
        return self.title


class Positions(models.Model):
    # В бедующем его нужно будет заменить на Json файл с очень точной настройкой каждой должности,
    # но это уже после создания большей части функционала (это про weight)
    class Weight(models.IntegerChoices):
        FULL_ACCESS = 1, 'Full access'
        PARTIAL_ACCESS = 2, 'Partial access'
        OBSERVE = 3, 'Observer'

    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='positions')
    title = models.CharField(max_length=40)
    weight = models.SmallIntegerField(choices=Weight.choices, default=Weight.PARTIAL_ACCESS)
    json_with_optional_info = models.JSONField(blank=True, default=dict)

    class Meta:
        unique_together = ['company_id', 'title']

    def __str__(self):
        return self.title


class Project(models.Model):
    class DisplayTypes(models.IntegerChoices):
        ABSOLUTE = 1, 'Absolute'
        PARTIAL = 2, 'Partial'
        IN_PERCENTAGES = 3, 'In_percentages'
        NONE_DISPLAY = 4, 'None_display'

    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=40)
    project_creater = models.IntegerField()
    view_counter = models.IntegerField(choices=DisplayTypes.choices, default=DisplayTypes.NONE_DISPLAY)
    json_info_with_access_level = models.JSONField(blank=True, default=dict)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class EmployeeCompany(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    # возможно models.SET_NULL не лучшая идея
    position_id = models.ForeignKey(Positions, on_delete=models.SET_NULL, null=True, blank=True)
    department_id = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    # json_with_employee_info = models.JSONField(blank=True, default=dict)

    class Meta:
        indexes = [
            models.Index(fields=['company_id', 'employee_id'])
        ]


class Chat(models.Model):
    title = models.CharField(max_length=250)
    employees = models.ManyToManyField(Employee, related_name='chats')

    class Meta:
        ordering = ['title']


class Message(models.Model):
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='messages')
    last_update = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    json_with_content = models.JSONField(blank=True, default=dict)


class Customization(models.Model):
    customisation_id = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True, related_name='customization')
    color_scheme = models.CharField(max_length=40, default='')
    font_size = models.CharField(max_length=40, default='')
    background = models.CharField(max_length=40, default='')


class Task(models.Model):
    class StatusType(models.IntegerChoices):
        ACCEPTED = 1, 'Accepted'
        WORK = 2, 'Work'
        INSPECTION = 3, 'Inspection'
        REVISION = 4, 'Revision'

    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=40)
    text = models.TextField(blank=True, null=True)
    parent_id = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='childs')
    status = models.IntegerField(choices=StatusType.choices, default=StatusType.WORK)
    json_with_employee_info = models.JSONField(blank=True, default=dict)
    user_category = models.ManyToManyField('Category', through='Taskboard', related_name='tasks')

    class Meta:
        ordering = ['project_id', 'title']

    def __str__(self):
        return self.title


class TaskImage(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/%H/')
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='images')

    class Meta:
        order_with_respect_to = 'task_id'


class TaskFile(models.Model):
    file = models.ImageField(upload_to='files/%Y/%m/%d/%H/')
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files')

    class Meta:
        order_with_respect_to = 'task_id'


class Subtasks(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=40)
    text = models.TextField(blank=True, null=True)
    status_yes_no = models.BooleanField(default=False)
    json_with_employee_info = models.JSONField(blank=True, default=dict)

    class Meta:
        ordering = ['task_id', 'title']

    def __str__(self):
        return self.title


class SubtaskImage(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/%H/')
    subtask_id = models.ForeignKey(Subtasks, on_delete=models.CASCADE, related_name='images')

    class Meta:
        order_with_respect_to = 'subtask_id'


class SubtaskFile(models.Model):
    file = models.ImageField(upload_to='images/%Y/%m/%d/%H/')
    subtask_id = models.ForeignKey(Subtasks, on_delete=models.CASCADE, related_name='files')

    class Meta:
        order_with_respect_to = 'subtask_id'


class Category(models.Model):
    title = models.CharField(max_length=40)
    employee_id = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE, related_name='categories')
    project_personal_notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['title']
        unique_together = ['title', 'employee_id']

    def __str__(self):
        return self.title


class UserProjectTime(models.Model):
    json_with_time_and_name_info = models.JSONField(blank=True, default=dict)


class Taskboard(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='taskboards')
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    task_personal_notes = models.JSONField(blank=True, default=dict)
    json_with_subtask_and_subtask_personal_note = models.JSONField(blank=True, default=dict)

    class Meta:
        ordering = ['title']


class CompanyEvent(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=40)
    description = models.TextField(blank=True, null=True)
    json_with_employee_info = models.JSONField(blank=True, default=dict)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()

    class Meta:
        ordering = ['-time_start']


class CompanyEventImage(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/%H/')
    company_event = models.ForeignKey(CompanyEvent, on_delete=models.CASCADE, related_name='images')

    class Meta:
        order_with_respect_to = 'company_event'


class CompanyEventFile(models.Model):
    file = models.FileField(upload_to='files/%Y/%m/%d/%H/')
    company_event = models.ForeignKey(CompanyEvent, on_delete=models.CASCADE, related_name='files')

    class Meta:
        order_with_respect_to = 'company_event'

