from django.utils import timezone

from . import models


def get_deadline_status(deadline):
    time_end = deadline.time_end
    now = timezone.now()
    if time_end is None:
        return models.UserTimeCategory.Status.PERMANENT

    time_interval = (time_end - now).total_seconds()
    day = 86400     # sec

    if time_interval < 0:
        return models.UserTimeCategory.Status.OVERTIMED
    elif time_interval <= day:
        return models.UserTimeCategory.Status.TODAY
    elif time_interval <= 2 * day:
        return models.UserTimeCategory.Status.TOMORROW
    elif time_interval <= 7 * day:
        return models.UserTimeCategory.Status.WEEK
    elif time_interval <= 30 * day:
        return models.UserTimeCategory.Status.MONTH
    else:
        return models.UserTimeCategory.Status.NOT_SOON
