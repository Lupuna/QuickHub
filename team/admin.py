from django.contrib import admin
from . import models


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    list_display_links = ('id', 'email')


@admin.register(models.LinksResources)
class LinksResourcesAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee_id', 'link')


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner_id')


@admin.register(models.Positions)
class PositionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_id', 'title')


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_id', 'title')


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'title')


@admin.register(models.Subtasks)
class SubtasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_id', 'title')


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_id', 'employee_id')


@admin.register(models.EmployeeCompany)
class EmployeeCompanyAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'employee_id', 'position_id', 'department_id')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'employee_id')


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent_id', 'supervisor')


@admin.register(models.CompanyEvent)
class CompanyEventImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_start', 'time_end')
