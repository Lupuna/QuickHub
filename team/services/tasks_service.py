from django.utils import timezone
from django.db.models import QuerySet

from .. import models, forms
from user_project_time import (
    models as user_project_time_models, 
    services as user_project_time_services,
)
from user_project import (
    models as user_project_models, 
    services as user_project_services,
)

# /// ФУНКЦИИ ДЛЯ ЗАДАЧ ///

def employee_info(task: models.Task, 
                form: forms.TaskCreationForm,
                appoint=None) -> dict:
    '''Заполнение json_with_employee_info объекта Task данными о работниках'''
    if appoint is None:
        appoint = task.json_with_employee_info['appoint'][0]
    else:
        appoint = appoint.email

    json_with_employee_info = {
        'appoint': [appoint],
        'responsible': [i.email for i in form.cleaned_data.get('responsible')],
        'executor': [i.email for i in form.cleaned_data.get('executor')]
    }
    return json_with_employee_info

# /// ADD ///

def add_task_to_user_categories(task: models.Task,
                                user: models.Employee) -> None:
    '''
    Добавление задачи в категорию "Мои задачи" для user и в категорию
    задач по срокам
    '''
    user.tasks.add(task)
    user.categories.get(title='Мои задачи').tasks.add(task)
    user.time_categories.get(status=task.time_status).tasks.add(task)

# /// SET ///

@user_project_time_services.set_user_time_category
@user_project_services.set_user_category
def set_executors(task: models.Task, 
                executors: QuerySet[models.Employee]) -> models.Task:
    '''Назначение исполнителей на задачу'''
    task.executors.set(executors, clear=True)
    return task

# /// UPDATE ///

@user_project_time_services.set_user_time_category
def update_task_deadline(task: models.Task,
                         start=None,
                         end=None,
                         **kwargs) -> models.Task:
    '''Изменение сроков задачи'''
    if start is None:
        start = timezone.now()
    task.time_start = start
    task.time_end = end
    task.save()
    return task


def update_task(task: models.Task,
                form: forms.TaskCreationForm,
                *args,
                **kwargs) -> models.Task:
    '''Обновление полей задачи данными из формы form'''
    task.text = form.cleaned_data.get('text')
    task.title = form.cleaned_data.get('title')
    task.parent_id = form.cleaned_data.get('parent_id')
    task.project_id = kwargs.get('project')
    task.save()
    
    time_start = form.cleaned_data.get('time_start')
    time_end = form.cleaned_data.get('time_end')
    executors = form.cleaned_data.get('executor')

    task = update_task_deadline(
        task=task,
        executors=executors,
        start=time_start,
        end=time_end
    )

    set_executors(task=task, executors=executors)

    return task
