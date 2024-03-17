from django.db import models



class TaskDeadline(models.Model):
    task = models.ForeignKey(
        to='team.Task', 
        on_delete=models.CASCADE, 
        related_name='deadline'
    )
    time_category = models.ForeignKey(
        to='UserTimeCategory',
        on_delete=models.CASCADE,
        related_name='deadlines',
    )
    time_start = models.DateTimeField(
        null=True, 
        blank=True
    )
    time_end = models.DateTimeField(
        null=True, 
        blank=True
    )

    class Meta:
        ordering = ['-time_start']
    

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
        to='team.Employee', 
        on_delete=models.CASCADE, 
        related_name='time_categories'
    )
    tasks = models.ManyToManyField(
        to='team.Task',
        through='TaskDeadline',
        related_name='time_categories'
    )
    status = models.CharField(
        max_length=9, 
        choices=Status.choices,
        default=Status.PERMANENT
    )

    def __str__(self):
        return f'{self.employee.email} : {self.status}'
    
    class Meta:
        unique_together = ['employee', 'status']