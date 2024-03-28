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
