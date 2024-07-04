import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from team.models import Employee, Company, Department, Positions, EmployeeCompany, Project, Task, Subtasks
from team import utils
from django.contrib.auth.hashers import make_password
import json

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        # Generate Companies
        companies = []
        for i in range(10):
            company = Company.objects.create(
                title=f'Company_{i}',
                owner_id=random.randint(1, 100)
            )
            companies.append(company)
        self.stdout.write(self.style.SUCCESS('Companies created'))

        # Generate Employees
        employees = []
        for i in range(100):
            employee = Employee.objects.create(
                username=f'user_{i}',
                name=f'User_{i}',
                email=f'user_{i}@example.com',
                password=make_password('password123'),
                city=f'City_{i}',
                birthday=timezone.now() - timezone.timedelta(days=random.randint(7000, 25000)),
                telephone=f'123456789{i}',
                online_status=bool(random.getrandbits(1)),
                json_with_settings_info=json.dumps({"theme": "dark" if i % 2 == 0 else "light"}),
            )
            employees.append(employee)
        self.stdout.write(self.style.SUCCESS('Employees created'))

        # Generate Positions
        positions = []
        for i in range(10):
            for company in companies:
                position = Positions.objects.create(
                    company_id=company,
                    title=f'Position_{i}',
                    weight=random.choice([1, 2, 3])
                )
                positions.append(position)
        self.stdout.write(self.style.SUCCESS('Positions created'))

        # Generate Departments
        departments = []
        for i in range(10):
            for company in companies:
                department = Department.objects.create(
                    company_id=company,
                    title=f'Department_{i}',
                    supervisor=random.choice(employees)
                )
                departments.append(department)
        self.stdout.write(self.style.SUCCESS('Departments created'))

        # Generate EmployeeCompany relations
        for employee in employees:
            company = random.choice(companies)
            EmployeeCompany.objects.create(
                company_id=company,
                employee_id=employee,
                position_id=random.choice(positions),
                department_id=random.choice(departments)
            )
        self.stdout.write(self.style.SUCCESS('EmployeeCompany relations created'))

        # Generate Projects
        projects = []
        for i in range(10):
            for company in companies:
                project = Project.objects.create(
                    company_id=company,
                    title=f'Project_{i}',
                    project_creater=random.randint(1, 100),
                    view_counter=random.choice([1, 2, 3, 4]),
                    json_info_with_access_level=json.dumps({"level": "high" if i % 2 == 0 else "low"}),
                    task_status=utils.get_task_status()
                )
                projects.append(project)
        self.stdout.write(self.style.SUCCESS('Projects created'))

        # Generate Tasks
        tasks = []
        for i in range(100):
            project = random.choice(projects)
            task = Task.objects.create(
                project_id=project,
                title=f'Task_{i}',
                text=f'This is the description for task {i}.',
                parent_id=None,
                json_with_employee_info=json.dumps({"assigned_to": f'user_{random.randint(0, 99)}'}),
                task_status=None,  # will be set in save method
                time_start=timezone.now(),
                time_end=timezone.now() + timezone.timedelta(days=random.randint(1, 30))
            )
            tasks.append(task)
        self.stdout.write(self.style.SUCCESS('Tasks created'))

        # Generate Subtasks
        for i in range(100):
            task = random.choice(tasks)
            Subtasks.objects.create(
                task_id=task,
                title=f'Subtask_{i}',
                text=f'This is the description for subtask {i}.',
                status_yes_no=bool(random.getrandbits(1)),
                json_with_employee_info=json.dumps({"assigned_to": f'user_{random.randint(0, 99)}'})
            )
        self.stdout.write(self.style.SUCCESS('Subtasks created'))