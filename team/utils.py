from django.utils import timezone
from . import models


def create_base_settings_json_to_employee():
    js = {
        "settings_info_about_company_employee": ["image", "name", "email", "telephone", "position_title"]
    }
    return js


def create_employee_list(company_id: int) -> list:
    return company_id.employees.distinct()


def add_new_employee(company_id, employee_id):
    company_id = models.Company.objects.get(id=company_id)
    employee_id = models.Employee.objects.get(id=employee_id)
    new_employee = models.EmployeeCompany(company_id=company_id, employee_id=employee_id)
    new_employee.save()


def set_position(employee_id, company_id, position_id):
    user = models.Employee.objects.get(id=employee_id)
    position = models.Positions.objects.get(id=position_id)
    company = models.Company.objects.get(id=company_id)
    employee = models.EmployeeCompany.objects.get(employee_id=user, company_id=company)
    employee.position_id = position
    employee.save()


def get_task_status():
    return {'status': {'Accepted': 1, 'Work': 2, 'Inspection': 3, 'Revision': 4}}


def get_deadline_status(deadline):
    time_end = deadline.time_end
    now = timezone.now()
    if time_end is None:
        return 'Permanent'

    time_interval = (time_end - now).total_seconds()
    day = 86400     # sec

    if time_interval < 0:
        return 'Overtimed'
    elif time_interval <= day:
        return 'Today'
    elif time_interval <= 2 * day:
        return 'Tomorrow'
    elif time_interval <= 7 * day:
        return 'Week'
    elif time_interval <= 30 * day:
        return 'Month'
    else:
        return 'Not_soon'
