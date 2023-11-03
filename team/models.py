from django.db import models
from django.contrib.auth.models import AbstractUser


def base_employee_optional():
    return {
        'city': '',
        'birthday': '',
        'LinksResources': [],
        'telephone': '',
    }


def base_employee_settings():
    return {}


def base_company_department():
    return {}


def base_company_settings():
    return {}


def base_employeecompany_info():
    return {}


def base_message_info():
    return {
        'text': '',
        'video': '',
        'voice': '',
        'photo': '',
    }


class Employee(AbstractUser):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40)
    email = models.EmailField(unique=True)
    json_with_optional_info = models.JSONField(default=base_employee_optional())
    json_with_settings_info = models.JSONField(default=base_employee_settings())

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'password']


class Company(models.Model):
    title = models.CharField(max_length=250)
    owner_id = models.IntegerField(
        help_text='Тут будет храниться id создателя компании(т. е. того человека, который будет платить)')
    json_with_department_info = models.JSONField(default=base_company_department())
    json_with_settings_info = models.JSONField(default=base_company_settings())

    class Meta:
        ordering = ['title']


class Positions(models.Model):
    # В бедующем его нужно будет заменить на Json файл с очень точной настройкой каждой должности,
    # но это уже после создания большей части функционала (это про weight)
    class Weight(models.IntegerChoices):
        FULL_ACCESS = 1, 'Full access'
        PARTIAL_ACCESS = 2, 'Partial access'
        OBSERVE = 3, 'Observer'

    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    weight = models.SmallIntegerField(choices=Weight.choices, default=Weight.PARTIAL_ACCESS)
    json_with_optional_info = models.JSONField(null=True)


class Project(models.Model):
    class DisplayTypes(models.IntegerChoices):
        ABSOLUTE = 1, 'Absolute'
        PARTIAL = 2, 'Partial'
        IN_PERCENTAGES = 3, 'In_percentages'
        NONE_DISPLAY = 4, 'None_display'

    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    view_counter = models.IntegerField(choices=DisplayTypes.choices, default=DisplayTypes.NONE_DISPLAY)
    json_info_with_access_level = models.JSONField(null=True)

    class Meta:
        ordering = ['title']


class EmployeeCompany(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    # возможно models.SET_NULL не лучшая идея
    position_id = models.ForeignKey(Positions, on_delete=models.SET_NULL)
    json_with_employee_info = models.JSONField(default=base_employeecompany_info())

    class Meta:
        indexes = [
            models.Index(fields=['company_id', 'employee_id'])
        ]


class Chat(models.Model):
    title = models.CharField(max_length=250)
    employees = models.ManyToManyField(Employee)

    class Meta:
        ordering = ['title']


class Message(models.Model):
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    json_with_content = models.JSONField(default=base_message_info())
