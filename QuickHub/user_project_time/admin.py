from django.contrib import admin
from . import models

@admin.register(models.TaskDeadline)
class TaskDeadlineAdmin(admin.ModelAdmin):
    list_display = ['task', 'time_category']
    list_filter = ['time_category']


@admin.register(models.UserTimeCategory)
class UserTimeCategoryAdmin(admin.ModelAdmin):
    list_display = ['employee', 'status']