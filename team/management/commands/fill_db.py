import random
from django.core.management.base import BaseCommand

from team.models import (
    Employee, Company, Department, Positions, 
    EmployeeCompany, Project, Task, Subtasks
)
from user_project.models import (
    Category, Taskboard
)
from user_project_time.models import (
    UserTimeCategory, TaskDeadline
)
from team.utils import create_base_settings_json_to_employee, get_task_status
from team.services.tasks_service import set_executors


class Command(BaseCommand):
    def handle(self, *args, **options):
        Employee.objects.exclude(username='admin').delete()
        Company.objects.all().delete()
        Task.objects.all().delete()

        employees = [Employee(username=f'User {i}', 
                              name=f'User {i}', 
                              email=f'user{i}@user.com', 
                              json_with_settings_info=create_base_settings_json_to_employee()) for i in range(1, 101)]
        Employee.objects.bulk_create(employees)

        time_categories = []
        categories = []
        for employee in Employee.objects.all():
            employee.set_password('1234')
            employee.categories.add(Category.objects.create(title='Мои задачи'))

            categories += [Category(title=f'Category {i}', 
                                employee_id=employee) for i in range(1, 6)]
            time_categories += [UserTimeCategory(status=status,
                                                 employee=employee) for status in UserTimeCategory.Status]

            employee.save()

        Category.objects.bulk_create(categories)
        UserTimeCategory.objects.bulk_create(time_categories)


        companies = [Company(title=f'Company {i}', owner_id=random.randint(1, 100)) for i in range(1, 21)]
        Company.objects.bulk_create(companies)

        positions = [Positions(title=f'Position {i}', 
                               weight=random.randint(1, 3),
                               company_id=random.choice(companies)) for i in range(1, 150)]
        Positions.objects.bulk_create(positions)

        departments = []
        for company in Company.objects.all():
            company.employees.set(random.sample(employees, random.randint(5, 15)))
            company.positions.set(random.sample(positions, random.randint(5, 12)))

            departments += [Department(title=f'Department {i}', 
                                        company_id=company,
                                        supervisor_id=company.employees.order_by('?')[0].id) for i in range(1, 5)]
                    
            projects_company = [Project(title=f'Project {i}', 
                            task_status=get_task_status(),
                            view_counter=random.randint(1, 4),
                            company_id=company,
                            project_creater=random.choice(list(company.employees.values_list('id', flat=True)))) for i in range(1, 7)]
            Project.objects.bulk_create(projects_company)
        
            tasks = [Task(title=f'Task {i}', 
                          text=f'Task {i}',
                          project_id=random.choice(projects_company)) for i in range(1, 10)]
            Task.objects.bulk_create(tasks)
            
            tasks_company = Task.objects.filter(project_id__in=company.projects.all())
            for task in tasks_company:
                set_executors(
                    task=task, 
                    executors=random.sample(list(company.employees.all()), random.randint(3, 5)),
                )

                list_executors = list(task.executors.values_list('email', flat=True))
                task.json_with_employee_info = {
                    'appoint': [random.choice(list_executors)],
                    'responsible': list_executors,
                    'executor': list_executors,
                }
                task.save()

            subtasks = [Subtasks(title=f'Subtask {i}', 
                                 text=f'Subtask {i}', 
                                 task_id=random.choice(tasks_company)) for i in range(1, 8)]
            Subtasks.objects.bulk_create(subtasks)

        Department.objects.bulk_create(departments)

        for employee in Employee.objects.all():
            employee.departments.set(
                random.sample(Department.objects.filter(company_id__in=employee.companies.all()), random.randint(1, 4)),
                through_defaults={
                    'position_id': random.choice(Positions.objects.filter(company_id__in=employee.companies.all())),
                }
            )
            