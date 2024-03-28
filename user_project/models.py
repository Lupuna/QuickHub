from django.db import models


class Category(models.Model):
    title = models.CharField(
        'Название', 
        max_length=40,
    )
    employee_id = models.ForeignKey(
        verbose_name='Работники',
        to='team.Employee', 
        null=True, 
        on_delete=models.CASCADE, 
        related_name='categories',
    )
    project_personal_notes = models.TextField(
        'Заметки', 
        blank=True, 
        null=True
    )
    tasks = models.ManyToManyField(
        verbose_name='Задачи',
        to='team.Task', 
        through='Taskboard', 
        related_name='user_category',
    )

    class Meta:
        ordering = ['title']
        unique_together = ['title', 'employee_id']

    def __str__(self):
        return self.title


class Taskboard(models.Model):
    category_id = models.ForeignKey(
        verbose_name='Категория',
        to='Category', 
        on_delete=models.CASCADE, 
        related_name='taskboards',
    )
    task_id = models.ForeignKey(
        verbose_name='Задачи',
        to='team.Task', 
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        'Категория',
        max_length=40
    )
    task_personal_notes = models.JSONField(
        'Заметки',
        blank=True, 
        default=dict
    )
    json_with_subtask_and_subtask_personal_note = models.JSONField(
        'Подзадачи',
        blank=True, 
        default=dict
    )

    class Meta:
        ordering = ['title']
        unique_together = ['category_id', 'task_id']
