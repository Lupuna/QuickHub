from django.db.models import QuerySet

from . import models as user_project_models
from team import models as team_models

# /// DECORATORS ///

def set_user_category(func: callable) -> callable:
    '''Добавление задачи в категорию "Мои задачи" для всех исполнителей'''
    def wrapper(task: team_models.Task,
                executors: QuerySet[team_models.Task], 
                *args, **kwargs) -> team_models.Task:
        task = func(task, executors)
        categories = user_project_models.Category.objects.filter(employee_id__in=executors, title='Мои задачи')
        task.user_category.set(categories, clear=True)
        return task
    
    return wrapper

# /// CREATE ///

def create_category(user: team_models.Task, **kwargs) -> user_project_models.Category:
    '''Создание пользовательской категории'''
    return user_project_models.Category.objects.create(employee_id=user, **kwargs)


def create_taskboard(category: user_project_models.Category, 
                     tasks: QuerySet[team_models.Task], **kwargs) -> user_project_models.Taskboard | None:
    '''
    Создание отображения категории задач пользователя для доски
    '''
    tasks = tasks.prefetch_related('subtasks').only('id', 'text')
    set_tasks_to_category(category=category, tasks=tasks)
    taskboard = None
    for task in tasks:
        taskboard = user_project_models.Taskboard(
            category_id=category,
            task_id=task,
            title=category.title,
            task_personal_notes={
                'notes': kwargs.get('notes'),
                'task_notes': task.text
            }
        )
        subtasks = task.subtasks.only('id', 'text')
        for subtask in subtasks:
            taskboard.json_with_subtask_and_subtask_personal_note[subtask.id] = subtask.text
        taskboard.save()
    return taskboard

# /// DELETE ///

def set_tasks_to_category(category: user_project_models.Category, 
                        tasks: QuerySet[team_models.Task], **kwargs) -> None:
    '''Назначение задач в категорию'''
    category.tasks.set(tasks, clear=True)

# /// GET ///
    
def get_user_categories(user: team_models.Employee, **kwargs):
    '''Получение всех категорий задач пользователя вместе с полями'''
    return user.categories.prefetch_related(
            'tasks__executors',
            'tasks__subtasks',
            'tasks__project_id__company_id',
            'tasks__deadline__time_category',
            # 'tasks__time_categories',
        )
