from django.utils import timezone
from django.db.models import QuerySet

from team import models as team_models
from . import models as user_project_time_models
from . import utils as user_project_time_utils

# /// DECORATORS ///

def update_time_category_decorator(func: callable) -> callable:
    '''Обновление статуса срока задачи. Задача помещается в другую категорию для пользователя user
    в зависимости от срока
    '''
    def wrapper(user: team_models.Employee, 
                task:team_models.Task, 
                start=None, 
                end=None, *args, **kwargs):
        deadline = func(user, task, start, end, *args, **kwargs)
        status = deadline.get_status
        time_category = user.time_categories.get(status=status)
        deadline.set_status = status
        deadline.time_category = time_category
        deadline.save(*args, **kwargs)
        return deadline
    
    return wrapper

# /// CREATE ///

# @update_time_category_decorator
def create_task_deadline(user: team_models.Employee,
                        task: team_models.Task , 
                        *args, **kwargs) -> user_project_time_models.TaskDeadline:
    '''Создание записи в TaskDeadline со связью категории UserTimeCategory пользователя'''
    deadline = user_project_time_models.TaskDeadline(task=task)
    return deadline


def create_time_category(user: team_models.Employee, **kwargs) -> user_project_time_models.UserTimeCategory:
    return user_project_time_models.UserTimeCategory.objects.create(employee=user, **kwargs)

# /// UPDATE ///

@update_time_category_decorator
def update_deadline(user: team_models.Employee, 
                    task: team_models.Task, 
                    start=None, 
                    end=None, 
                    *args, **kwargs):
    '''Обновление сроков дедлайна и смена категории для пользователя'''
    deadline = user_project_time_models.TaskDeadline.objects.get(time_category__employee=user, task=task)
    if start:
        deadline.time_start = start
    else:
        deadline.time_start = timezone.now()
    deadline.time_end = end
    deadline.save(*args, **kwargs)
    return deadline


def update_deadlines_for_executors(task: team_models.Task,
                                   start=None,
                                   end=None,
                                   *args, **kwargs) -> None:
    '''Обновление дедлайнов для всех исполнителей задачи'''
    executors = task.executors.all()
    for user in executors:
        update_deadline(user=user, task=task, start=start, end=end)
    

# /// GET /// 

def get_user_time_categories(user: team_models.Employee, **kwargs):
    '''Получение категорий сроков пользователя user вместе со связанными полями'''
    return user.time_categories.prefetch_related(
            'tasks',
            'tasks__executors',
            'tasks__subtasks',
            'tasks__project_id__company_id',
        )


def _change_user_task_time_category(task: team_models.Task,
                                    time_category: user_project_time_models.UserTimeCategory,
                                    *args,
                                    **kwargs):
    deadline = task.deadline.get(time_category__employee=time_category.employee)
    deadline.time_category = time_category
    deadline.save(*args, **kwargs)

    
def change_task_time_categories(task: team_models.Task, *args, **kwargs):
    ''''''
    status = task.time_status
    executors = task.executors.prefetch_related(
        'time_categories',
        'time_categories__employee',
    ).only('id')
    for user in executors:
        time_category = user.time_categories.only('id', 'employee').get(status=status)
        _change_user_task_time_category(task=task, time_category=time_category)