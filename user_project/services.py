from django.db.models import QuerySet

from . import models as user_project_models
from team import models as team_models


# /// CREATE ///

def create_category(user: team_models.Task, **kwargs) -> user_project_models.Category:
    return user_project_models.Category.objects.create(employee_id=user, **kwargs)


def create_taskboard(category: user_project_models.Category, 
                     tasks: QuerySet[team_models.Task], **kwargs) -> user_project_models.Taskboard:
    '''
    Создание отображения категории задач пользователя для доски
    '''
    tasks = tasks.prefetch_related('subtasks')
    delete_unmarked_tasks_from_taskboard(category=category, tasks=tasks)

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
        subtasks = task.subtasks.all()
        for subtask in subtasks:
            taskboard.json_with_subtask_and_subtask_personal_note[subtask.id] = subtask.text
        taskboard.save()
    return taskboard

# /// DELETE ///

def delete_unmarked_tasks_from_taskboard(category: user_project_models.Category, 
                                        tasks: QuerySet[team_models.Task], **kwargs) -> None:
    '''Удаление из пользовательской категории неотмеченных в форме задач'''
    user_project_models.Taskboard.objects\
        .filter(category_id=category)\
        .exclude(id__in=tasks.values_list('id'))\
        .delete()

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