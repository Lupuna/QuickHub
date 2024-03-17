from . import models, utils



def update_time_category_decorator(func: callable):
    '''Обновление статуса срока задачи. Задача помещается в другую категорию для пользователя user
    пользователя в зависимости от срока
    '''
    def wrapper(user, task: models.TaskDeadline, start=None, end=None, *args, **kwargs):
        deadline = func(user, task, start, end, *args, **kwargs)
        status = utils.get_deadline_status(deadline)
        time_category = user.time_categories.get(status=status)
        deadline.time_category = time_category
        deadline.save(*args, **kwargs)
        return deadline
    
    return wrapper


@update_time_category_decorator
def create_TaskDeadline(user, task, *args, **kwargs) -> models.TaskDeadline:
    '''Создание записи в TaskDeadline со связью категории UserTimeCategory пользователя'''
    deadline = models.TaskDeadline(task=task)
    return deadline


@update_time_category_decorator
def update_deadline(user, task, start, end, *args, **kwargs):
    '''Обновление сроков дедлайна и смена категории'''
    deadline = models.TaskDeadline.objects.get(time_category__employee=user, task=task)
    deadline.time_start = start
    deadline.time_end = end
    deadline.save(*args, **kwargs)
    return deadline


def create_TimeCategory(user, **kwargs) -> models.UserTimeCategory:
    return models.UserTimeCategory.objects.create(employee=user, **kwargs)
