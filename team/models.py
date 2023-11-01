from django.db import models
from django.utils import timezone


class Employee(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40)
    email = models.EmailField(unique=True)
    #   поле password добавить позже
    json_with_optional_info = models.JSONField(null=True)
    json_with_settings_info = models.JSONField(null=True)

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'email')  # заменить email на password


class Company(models.Model):
    title = models.CharField(max_length=250)
    owner_id = models.IntegerField(help_text='Тут будет храниться id создателя компании(т. е. того человека, который будет платить)')
    json_with_department_info = models.JSONField(null=True)
    json_with_settings_info = models.JSONField(null=True)

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


class Task(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    


