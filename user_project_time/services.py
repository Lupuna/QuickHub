from django.utils import timezone
from django.db.models import QuerySet

from team import models as team_models
from . import models as user_project_time_models
from . import utils as user_project_time_utils

# /// DECORATORS ///

def set_user_time_category(func: callable) -> callable:
    '''Добавление задачи в нужную категорию времени для всех исполнителей'''
    def wrapper(task: team_models.Task,
                executors: team_models.Employee,
                *args, **kwargs) -> team_models.Task:
        task = func(task=task, executors=executors)
        time_caterories = user_project_time_models.UserTimeCategory.objects.filter(
            employee__in=executors, 
            status=task.time_status
        )
        task.time_categories.set(time_caterories)
        return task
    
    return wrapper


# /// CREATE ///


def create_time_category(user: team_models.Employee, **kwargs) -> user_project_time_models.UserTimeCategory:
    return user_project_time_models.UserTimeCategory.objects.create(employee=user, **kwargs)


# /// GET /// 

def get_user_time_categories(user: team_models.Employee, **kwargs):
    '''Получение категорий сроков пользователя user вместе со связанными полями'''
    return user.time_categories.prefetch_related(
            'tasks',
            'tasks__executors',
            'tasks__subtasks',
            'tasks__project_id__company_id',
        )