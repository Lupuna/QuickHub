from . import models


def create_category(user, **kwargs) -> models.Category:
    return models.Category.objects.create(employee_id=user, **kwargs)
