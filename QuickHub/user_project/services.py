from django.db.models import QuerySet

from . import models
import team


def set_user_category(
    task: team.models.Task,
    executors: QuerySet[team.models.Task],
    default="Мои задачи"
) -> team.models.Task:
    """Добавление задачи в категорию "Мои задачи" для всех исполнителей"""
    categories = models.Category.objects.filter(employee_id__in=executors, title=default)
    task.user_category.set(categories, clear=True)
    return task


def create_category(user: team.models.Task, **kwargs) -> models.Category:
    """Создание пользовательской категории"""
    return models.Category.objects.create(employee_id=user, **kwargs)


def create_taskboards(category: models.Category,
                      tasks: QuerySet[team.models.Task], **kwargs) -> None:
    """
    Создание отображения категории задач пользователя для доски
    """
    tasks = tasks.prefetch_related('subtasks').only('id', 'text')
    set_tasks_to_category(category=category, tasks=tasks, title=str(category.title))
    for task in tasks:
        taskboard = models.Taskboard.objects.get(
            category_id=category,
            task_id=task,
        )
        taskboard.task_personal_notes = {
            'notes': kwargs.get('notes'),
            'task_notes': task.text
        }
        subtasks = task.subtasks.only('id', 'text')
        for subtask in subtasks:
            taskboard.json_with_subtask_and_subtask_personal_note[subtask.id] = subtask.text
        taskboard.save()


def set_tasks_to_category(category: models.Category,
                          tasks: QuerySet[team.models.Task], **kwargs) -> None:
    """Назначение задач в категорию"""
    category.tasks.set(tasks, clear=True, through_defaults=kwargs)


def get_user_categories(user: team.models.Employee):
    """Получение всех категорий задач пользователя вместе с полями"""
    return user.categories.prefetch_related(
        'tasks__executors',
        'tasks__subtasks',
        'tasks__project_id__company_id',
        'tasks__deadline__time_category',
    )
