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
    time_start = models.DateTimeField(
        'Начало задачи',
        null=True, 
        blank=True
    )
    time_end = models.DateTimeField(
        'Конец срока',
        null=True, 
        blank=True
    )
    status = models.CharField(
        'Статус',
        max_length=9, 
        choices=UserTimeCategory.Status.choices,
        default=UserTimeCategory.Status.PERMANENT
    )

    class Meta:
        ordering = ['-time_start']

    @property
    def get_status(self):
        '''
        Получение статуса срока задачи на текущий момент времени
        '''
        time_end = self.time_end
        now = timezone.now()
        
        if time_end is None:
            return UserTimeCategory.Status.PERMANENT

        time_interval = (time_end - now).days

        if time_interval < 0:
            return UserTimeCategory.Status.OVERTIMED
        elif time_interval <= 1:
            return UserTimeCategory.Status.TODAY
        elif time_interval < 2:
            return UserTimeCategory.Status.TOMORROW
        elif time_interval < 7:
            return UserTimeCategory.Status.WEEK
        elif time_interval < 31:
            return UserTimeCategory.Status.MONTH
        else:
            return UserTimeCategory.Status.NOT_SOON
        
    @get_status.setter
    def set_status(self, status):
        self.status = status
