from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from . import forms, models, utils

creator = 'team/main_functionality/includes/creator.html'

def sign_up(request):
    if request.method == 'POST':
        form = forms.CustomUserCreationFrom(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse_lazy('team:homepage'))
    else:
        form = forms.CustomUserCreationFrom()

    context = {'form': form}
    return render(request, 'registration/sign_up.html', context)


@login_required(login_url=reverse_lazy('team:login'))
def homepage(request):
    context = {
        # 'user': request.user, 
    }
    return render(request, 'team/main_functionality/homepage.html', context)


@login_required(login_url=reverse_lazy('team:login'))
def create_company(request):
    if request.method == 'POST':
        form = forms.CompanyCreationForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner_id = request.user.id
            company.save()
            utils.add_new_employee(company.id, request.user.id)
            return redirect(reverse_lazy('team:homepage'))
    else:
        form = forms.CompanyCreationForm()

    context = {
        'form': form,
        'title': 'QuickHub: Company-create',
       }
    return render(request, creator, context)


@login_required(login_url=reverse_lazy('team:login'))
def create_project(request, id):
    try:
        company_id = models.Company.objects.get(id=id)
    except ObjectDoesNotExist:
        return redirect(reverse_lazy('team:homepage'))
    if request.method == 'POST':
        form = forms.ProjectCreationForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.project_creater = request.user.id
            project.company_id = company_id
            project.save()
            return redirect(reverse_lazy('team:homepage'))
    else:
        form = forms.ProjectCreationForm()

    context = {
        'form': form,
        'title': 'QuickHub: Project-create'
        }
    return render(request, creator, context)


@login_required(login_url=reverse_lazy('team:login'))
def create_task(request, company_id, project_id):
    try:
        company_id = models.Company.objects.get(id=company_id)
        project_id = models.Project.objects.get(id=project_id)
        user = models.Employee.objects.get(id=request.user.id)
    except ObjectDoesNotExist:
        return redirect(reverse_lazy('team:homepage'))
    if request.method == 'POST':
        form = forms.TaskCreationForm(company_id, project_id.id, request.POST, request.FILES)
        if form.is_valid():
            task = models.Task()
            task.json_with_employee_info = {
                'appoint': [request.user.email],
                'responsible': [i.email for i in form.cleaned_data.get('responsible')],
                'executor': [i.email for i in form.cleaned_data.get('executor')]
            }
            task.project_id = project_id
            task.text = form.cleaned_data.get('text')
            task.title = form.cleaned_data.get('title')
            task.save()

            user.tasks.add(task)

            for f in request.FILES.getlist('files'): models.TaskFile.objects.create(file=f, task_id=task)
            for i in request.FILES.getlist('images'): models.TaskImage.objects.create(image=i, task_id=task)
            return redirect(reverse_lazy('team:homepage'))
    else:
        form = forms.TaskCreationForm(company_id, project_id.id)

    context = {
        'form': form,
        'title': 'QuickHub: Task-create',
       }
    return render(request, creator, context)


@login_required(login_url=reverse_lazy('team:login'))
def create_subtask(request, company_id, project_id, task_id):
    try:
        company_id = models.Company.objects.get(id=company_id)
        project_id = models.Project.objects.get(id=project_id)
        task_id = models.Task.objects.get(id=task_id)
    except ObjectDoesNotExist:
        return redirect(reverse_lazy('team:homepage'))
    if request.method == 'POST':
        form = forms.SubtaskCreationForm(company_id, request.POST, request.FILES)
        if form.is_valid():
            subtask = models.Subtasks()
            subtask.json_with_employee_info = {
                'appoint': [request.user.email],
                'responsible': [i.email for i in form.cleaned_data.get('responsible')],
                'executor': [i.email for i in form.cleaned_data.get('executor')]
            }
            subtask.task_id_id = task_id.id
            subtask.text = form.cleaned_data.get('text')
            subtask.title = form.cleaned_data.get('title')
            subtask.save()
            for f in request.FILES.getlist('files'): models.SubtaskFile.objects.create(file=f, subtask_id=subtask)
            for i in request.FILES.getlist('images'): models.SubtaskImage.objects.create(image=i, subtask_id=subtask)
            return redirect(reverse_lazy('team:homepage'))
    else:
        form = forms.SubtaskCreationForm(company_id)

    context = {
        'form': form,
        'title': 'QuickHub: Subtask-create',
        }
    return render(request, creator, context)


@login_required(login_url=reverse_lazy('team:login'))
def check_employee(request, company_id):
    try:
        company_id = models.Company.objects.get(id=company_id)
    except ObjectDoesNotExist:
        return redirect(reverse_lazy('team:homepage'))

    info_filter_about_employee = request.user.json_with_settings_info["settings_info_about_company_employee"]
    employees = models.Employee.objects.filter(
        id__in=models.EmployeeCompany.objects.filter(company_id=company_id).values('employee_id'))

    info_about_employees = []
    for employee in employees:
        info_about_employee = dict(
            filter(lambda x: x[0] in info_filter_about_employee, employee.get_all_info().items()))
        for link in models.LinksResources.objects.filter(employee_id=employee.id):
            if link.title in info_filter_about_employee:
                info_about_employee.update(link.get_info())

        if 'position_title' in info_filter_about_employee:
            position = models.Positions.objects.filter(
                id__in=models.EmployeeCompany.objects.filter(Q(employee_id=employee.id) & Q(company_id=company_id)))
            if position:
                position = position[0].title
            else:
                position = None
            info_about_employee.update({'position_title': position})

        if 'department' in info_filter_about_employee:
            department = models.Department.objects.filter(
                id__in=models.EmployeeCompany.objects.filter(Q(employee_id=employee.id) & Q(company_id=company_id))
            )
            if department:
                department = department[0].title
            else:
                department = None
            info_about_employee.update({'department': department})

        info_about_employees.append(info_about_employee)

    paginator = Paginator(info_about_employees, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'id': company_id.id}
    return render(request, 'team/main_functionality/view_company_employees.html', context)


@login_required(login_url=reverse_lazy('team:login'))
def choice_parameters(request, company_id):
    if request.method == 'POST':
        form = forms.ChoiceEmployeeParametersForm(request.POST)
        if form.is_valid():
            request.user.json_with_settings_info["settings_info_about_company_employee"] = []
            for item, flag in form.cleaned_data.items():
                if flag: request.user.json_with_settings_info["settings_info_about_company_employee"].append(item)
                request.user.save()
            return redirect(reverse_lazy('team:check_employee', kwargs={'company_id': company_id}))

    else:
        form = forms.ChoiceEmployeeParametersForm()

    context = {
        'form': form,
        'title': 'QuickHub: Company-create',
        'button': 'Choice'       
        }
    return render(request, creator, context)


def add_new_employee(company_id, employee_id):
    company_id = models.Company.objects.get(id=company_id)
    employee_id = models.Employee.objects.get(id=employee_id)
    new_employee = models.EmployeeCompany(company_id=company_id, employee_id=employee_id)
    new_employee.save()


@login_required(login_url=reverse_lazy('team:login'))
def create_category(request):
    if request.method == 'POST':
        form = forms.CategoryCreationForm(request.POST)

        if form.is_valid():
            user_proj = form.save(commit=False)
            user_proj.title = form.cleaned_data.get('title')
            user_proj.employee_id = models.Employee.objects.get(id=request.user.id)
            user_proj.project_personal_notes = form.cleaned_data.get('project_personal_notes')

            user_proj.save()

            return redirect(reverse_lazy('team:homepage'))
    else:
        form = forms.CategoryCreationForm()

    context = {
        'form': form,
        'title': 'QuickHub: Category-create',
    }
    return render(request, creator, context)


@login_required(login_url=reverse_lazy('team:login'))
def create_taskboard(request):
    if request.method == "POST":
        form = forms.TaskboardCreationForm(request.user.id, request.POST)

        if form.is_valid():
            tasks = models.Employee.objects.get(id=request.user.id).tasks.filter(id__in=form.cleaned_data.get('tasks'))
            category = form.cleaned_data.get('category')
            for task in tasks:
                upt = models.UserProjectTask()

                upt.user_project_id = category
                upt.task_id = task
                upt.title = str(category)
                upt.task_personal_notes = {
                    'notes': form.cleaned_data.get('text'),
                    'task_notes': task.text
                }

                try:
                    subtasks = models.Subtasks.objects.filter(task_id=task)
                    upt.json_with_subtask_and_subtask_personal_not = {
                        'subtasks': [subtask.id for subtask in subtasks],
                    }
                except ObjectDoesNotExist:
                    ...

                upt.save()
    else:
        form = forms.TaskboardCreationForm(request.user.id)

    context = {
        'form': form,
        'title': 'QuickHub: Taskboard-create',
    }
    return render(request, creator, context)


def taskboard(request):
    categories = models.UserProject.objects.filter(employee_id=request.user.id)

    cats = {}
    for cat in categories:
        cats[cat] = models.Employee.objects.get(id=request.user.id).tasks \
            .filter(id__in=models.UserProjectTask.objects.filter(user_project_id=cat).values('task_id'))

    context = {
        'cats': cats,
    }
    return render(request, 'team/main_functionality/taskboard.html', context)


@login_required(login_url=reverse_lazy('team:login'))
def create_department(request, company_id):
    '''
    Создание отдела в компании
    '''
    try:
        company = models.Company.objects.get(id=company_id)
    except ObjectDoesNotExist:
        return redirect(reverse_lazy('team:homepage'))

    if request.method == 'POST':
        form = forms.DepartmentCreationForm(company_id, request.POST)

        if form.is_valid():
            department = models.Department()
            supervisor = models.Employee.objects.get(email=form.cleaned_data.get('supervisor'))

            department.title = form.cleaned_data.get('title')
            department.supervisor = supervisor.id
            department.company_id = models.Company.objects.get(id=company_id)
            try:
                department.parent_id = models.Department.objects \
                    .get(Q(title=form.cleaned_data.get('parent')) & Q(company_id=company_id))
            except ObjectDoesNotExist:
                department.parent_id = None

            department.save()

            user = models.EmployeeCompany.objects.get(employee_id=supervisor, company_id=company)
            user.department_id = department
            user.save()

            for employee in form.cleaned_data.get('employees'):
                user = models.EmployeeCompany.objects.get(employee_id=employee, company_id=company)
                user.department_id = department
                user.save()

            return redirect(reverse_lazy('team:homepage'))
    else:
        form = forms.DepartmentCreationForm(company_id)
    context = {
        'form': form,
        'title': 'QuickHub: Department-create'
    }
    return render(request, creator, context)


@login_required(login_url=reverse_lazy('team:homepage'))
def view_department(request, company_id, department_id):
    department = models.Department.objects.get(Q(company_id=company_id) & Q(id=department_id))
    supervisor = models.Employee.objects.get(id=department.supervisor)
    employees = models.Employee.objects \
        .filter(id__in=models.EmployeeCompany.objects \
                .filter(Q(department_id=department_id) & Q(company_id=company_id)).values('employee_id'))

    context = {
        'department': department,
        'employees': employees,
        'supervisor': supervisor,
    }
    return render(request, 'team/main_functionality/view_department.html', context)


@login_required(login_url=reverse_lazy('team:homepage'))
def create_position(request, company_id):
    try:
        company = models.Company.objects.get(id=company_id)
    except ObjectDoesNotExist:
        return redirect(reverse_lazy('team:homepage'))

    if request.method == 'POST':
        form = forms.PositionCreationForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.company_id = company
            position.json_with_optional_info = {
                'text': form.cleaned_data.get('text')
            }
            position.save()

            return redirect(reverse_lazy('team:homepage'))
    else:
        form = forms.PositionCreationForm()

    context = {
        'form': form,
        'title': 'QuickHub: Position-create',
    }
    return render(request, creator, context)


@login_required(login_url=reverse_lazy('team:homepage'))
def view_positions(request, company_id):
    try:
        company = models.Company.objects.get(id=company_id)
    except ObjectDoesNotExist:
        return redirect(reverse_lazy('team:homepage'))

    positions = models.Positions.objects.filter(company_id=company).all()

    context = {
        'company': company,
        'positions': positions,
    }
    return render(request, 'team/main_functionality/view_positions.html', context)
