from django.db import models
from django.urls import reverse
from django.utils import timezone


class UserTimeCategory(models.Model):
    class Status(models.TextChoices):
        OVERTIMED = 'Overtimed'
        TODAY = 'Today'
        TOMORROW = 'Tomorrow'
        WEEK = 'Week'
        MONTH = 'Month'
        NOT_SOON = 'Not_soon'
        PERMANENT = 'Permanent'

    employee = models.ForeignKey(
        verbose_name='Работник',
        to='team.Employee', 
        on_delete=models.CASCADE, 
        related_name='time_categories'
    )
    tasks = models.ManyToManyField(
        verbose_name='Задачи',
        to='team.Task',
        through='TaskDeadline',
        related_name='time_categories'
    )
    status = models.CharField(
        'Статус',
        max_length=9, 
        choices=Status.choices,
        default=Status.PERMANENT
    )

    def __str__(self):
        return self.status
    
    def get_absolute_url(self):
        return reverse('user_project_time:deadline_detail', kwargs={
            'status': self.status
        })


class TaskDeadline(models.Model):
    task = models.ForeignKey(
        verbose_name='Задачи',
        to='team.Task', 
        on_delete=models.CASCADE, 
        related_name='deadline'
    )
    time_category = models.ForeignKey(
        verbose_name='Категория срочности',
        to='UserTimeCategory',
        on_delete=models.CASCADE,
        related_name='deadlines',
    )