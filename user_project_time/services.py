from . import models


def create_TimeCategory(user, **kwargs) -> models.UserTimeCategory:
    return models.UserTimeCategory.objects.create(employee=user, **kwargs)