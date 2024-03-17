from . import models, utils


def create_TimeCategory(user, **kwargs) -> models.UserTimeCategory:
    return models.UserTimeCategory.objects.create(employee=user, **kwargs)


def create_TaskDeadline(user, task, **kwargs) -> models.TaskDeadline:
    '''Создание записи в TaskDeadline со связью категорию UserTimeCategory пользователя'''
    deadline = models.TaskDeadline(task=task)
    status = utils.get_deadline_status(deadline)
    time_category = user.time_categories.get(employee=user, status=status)
    deadline.time_category = time_category
    deadline.save()
    return deadline