from django.db import models
from team import models as team_models


class Category(models.Model):
    title = models.CharField(max_length=40)
    employee_id = models.ForeignKey(team_models.Employee, null=True, on_delete=models.CASCADE, related_name='categories')
    project_personal_notes = models.TextField(blank=True, null=True)
    tasks = models.ManyToManyField(team_models.Task, through='Taskboard', related_name='user_category')

    class Meta:
        ordering = ['title']
        unique_together = ['title', 'employee_id']

    def __str__(self):
        return self.title


class Taskboard(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='taskboards')
    task_id = models.ForeignKey(team_models.Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    task_personal_notes = models.JSONField(blank=True, default=dict)
    json_with_subtask_and_subtask_personal_note = models.JSONField(blank=True, default=dict)

    class Meta:
        ordering = ['title']
        unique_together = ['category_id', 'task_id']
