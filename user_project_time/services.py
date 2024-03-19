from django.db.models import QuerySet

from team import models as team_models
from . import models as user_project_time_models
from . import utils as user_project_time_utils

# /// DECORATORS ///

def update_time_category_decorator(func: callable) -> callable:
    '''Обновление статуса срока задачи. Задача помещается в другую категорию для пользователя user
    пользователя в зависимости от срока
    '''
    def wrapper(user: team_models.Employee, 
                task:team_models.Task, 
                start=None, 
                end=None, *args, **kwargs):
        deadline = func(user, task, start, end, *args, **kwargs)
        status = user_project_time_utils.get_deadline_status(deadline)
        time_category = user.time_categories.get(status=status)
        deadline.status = status
        deadline.time_category = time_category
        deadline.save(*args, **kwargs)
        return deadline
    
    return wrapper

# /// CREATE ///

@update_time_category_decorator
def create_task_deadline(user: team_models.Employee,
                        task: team_models.Task , *args, **kwargs) -> user_project_time_models.TaskDeadline:
    '''Создание записи в TaskDeadline со связью категории UserTimeCategory пользователя'''
    deadline = user_project_time_models.TaskDeadline(task=task)
    return deadline


def create_time_category(user: team_models.Employee, **kwargs) -> user_project_time_models.UserTimeCategory:
    return user_project_time_models.UserTimeCategory.objects.create(employee=user, **kwargs)

# /// UPDATE ///

@update_time_category_decorator
def update_deadline(user: team_models.Employee, 
                    task: team_models.Task, 
                    start, 
                    end, *args, **kwargs):
    '''Обновление сроков дедлайна и смена категории'''
    deadline = user_project_time_models.TaskDeadline.objects.get(time_category__employee=user, task=task)
    deadline.time_start = start
    deadline.time_end = end
    deadline.save(*args, **kwargs)
    return deadline

# /// GET /// 

def get_user_time_categories(user: team_models.Employee, **kwargs):
    '''Получение категорий сроков пользователя user вместе со связанными полями'''
    return user.time_categories.prefetch_related(
            'tasks__executors',
            'tasks__subtasks',
            'tasks__project_id__company_id',
            'tasks__deadline__time_category',
        )
    