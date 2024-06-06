from django.utils import timezone
from django.db.models import QuerySet

from .. import models, forms
import user_project as taskboards
import user_project_time as deadlines


def employee_info(task: models.Task,
                  form: forms.TaskCreationForm,
                  appoint=None) -> dict:
    """Заполнение json_with_employee_info объекта Task данными о работниках"""
    if appoint is None:
        appoint = task.json_with_employee_info['appoint']
    else:
        if isinstance(appoint, models.Employee):
            appoint = [appoint.email]
        elif isinstance(appoint, str):
            appoint = [appoint]

    json_with_employee_info = {
        'appoint': appoint,
        'responsible': [i.email for i in form.cleaned_data.get('responsible')],
        'executor': [i.email for i in form.cleaned_data.get('executor')]
    }
    return json_with_employee_info


def update_task(task: models.Task,
                form: forms.TaskCreationForm,
                project: models.Project = None) -> models.Task:
    """Обновление полей задачи данными из формы form"""
    task.text = form.cleaned_data.get('text')
    task.title = form.cleaned_data.get('title')
    task.parent_id = form.cleaned_data.get('parent_id')
    if project is not None:
        task.project_id = project
    task.save()

    time_start = form.cleaned_data.get('time_start')
    time_end = form.cleaned_data.get('time_end')
    executors = form.cleaned_data.get('executor')

    task = update_task_deadline(
        task=task,
        start=time_start,
        end=time_end
    )

    task = set_executors(task=task, executors=executors)
    task = deadlines.services.set_user_time_category(task=task, executors=executors)
    task = taskboards.services.set_user_category(task=task, executors=executors)
    return task


def set_executors(task: models.Task, executors: QuerySet[models.Employee]) -> models.Task:
    """Назначение исполнителей на задачу"""
    task.executors.set(executors, clear=True)
    return task


def update_task_deadline(
    task: models.Task,
    start=None,
    end=None,
) -> models.Task:
    """Изменение сроков задачи"""

    if start is None:
        start = timezone.now()
    task.time_start = start
    task.time_end = end
    task.save()
    return task
