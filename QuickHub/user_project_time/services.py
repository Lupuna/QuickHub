import team
from . import models


def set_user_time_category(
    task: team.models.Task,
    executors: team.models.Employee,
) -> team.models.Task:
    """Добавление задачи в нужную категорию времени для всех исполнителей"""

    time_caterories = models.UserTimeCategory.objects.filter(
        employee__in=executors,
        status=task.time_status
    )
    task.time_categories.set(time_caterories)
    return task


def create_time_category(user: team.models.Employee, **kwargs) -> models.UserTimeCategory:
    return models.UserTimeCategory.objects.create(employee=user, **kwargs)


def get_user_time_categories(user: team.models.Employee):
    """Получение категорий сроков пользователя user вместе со связанными полями"""
    return user.time_categories.prefetch_related(
            'tasks',
            'tasks__executors',
            'tasks__subtasks',
            'tasks__project_id__company_id',
        )