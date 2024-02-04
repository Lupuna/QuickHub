from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from . import forms, models, utils

creator = 'team/main_functionality/includes/creator.html'


class CreateCompany(LoginRequiredMixin, FormView):
    template_name = creator
    form_class = forms.CompanyCreationForm
    success_url = reverse_lazy('team:homepage')
    login_url = reverse_lazy('team:login')
    extra_context = {'title': 'QuickHub: Company-create'}

    def form_valid(self, form):
        company = form.save(commit=False)
        company.owner_id = self.request.user.id
        company.save()
        utils.add_new_employee(company.id, self.request.user.id)
        return super().form_valid(company)


class CreateProject(LoginRequiredMixin, utils.ModifiedFormView):
    template_name = creator
    success_url = reverse_lazy('team:homepage')
    login_url = reverse_lazy('team:login')
    form_class = forms.ProjectCreationForm
    extra_context = {'title': 'QuickHub: Project-create'}

    def form_valid(self, form):
        project = form.save(commit=False)
        project.project_creater = self.request.user.id
        project.company_id = self.kwargs['company_id']
        form.save()
        return super().form_valid(form)


class CreateTask(LoginRequiredMixin, utils.ModifiedFormView):
    login_url = reverse_lazy('team:login')
    template_name = creator
    success_url = reverse_lazy('team:homepage')
    form_class = forms.TaskCreationForm
    extra_context = {'title': 'QuickHub: Task-create'}

    def dispatch(self, request, *args, **kwargs):
        try:
            self.kwargs['user'] = models.Employee.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
            return redirect(reverse_lazy('team:homepage'))

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company_id'] = self.kwargs['company_id']
        kwargs['project_id'] = self.kwargs['project_id'].id
        return kwargs

    def form_valid(self, form):
        task = models.Task()
        task.json_with_employee_info = {
            'appoint': [self.kwargs['user'].email],
            'responsible': [i.email for i in form.cleaned_data.get('responsible')],
            'executor': [i.email for i in form.cleaned_data.get('executor')]
        }
        task.project_id = self.kwargs['project_id']
        task.text = form.cleaned_data.get('text')
        task.title = form.cleaned_data.get('title')
        task.save()

        self.kwargs['user'].tasks.add(task)

        for f in self.request.FILES.getlist('files'): models.TaskFile.objects.create(file=f, task_id=task)
        for i in self.request.FILES.getlist('images'): models.TaskImage.objects.create(image=i, task_id=task)
        return super().form_valid(task)


class CreateSubtask(LoginRequiredMixin, utils.ModifiedFormView):
    login_url = reverse_lazy('team:login')
    template_name = creator
    success_url = reverse_lazy('team:homepage')
    form_class = forms.SubtaskCreationForm
    extra_context = {'title': 'QuickHub: Subtask-create'}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company_id'] = self.kwargs['company_id']
        return kwargs

    def form_valid(self, form):
        subtask = models.Subtasks()
        subtask.json_with_employee_info = {
            'appoint': [self.request.user.email],
            'responsible': [i.email for i in form.cleaned_data.get('responsible')],
            'executor': [i.email for i in form.cleaned_data.get('executor')]
        }
        subtask.task_id_id = self.kwargs['task_id'].id
        subtask.text = form.cleaned_data.get('text')
        subtask.title = form.cleaned_data.get('title')
        subtask.save()
        for f in self.request.FILES.getlist('files'): models.SubtaskFile.objects.create(file=f, subtask_id=subtask)
        for i in self.request.FILES.getlist('images'): models.SubtaskImage.objects.create(image=i, subtask_id=subtask)
        return super().form_valid(subtask)


class ChoiceParameters(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('team:login')
    template_name = 'team/main_functionality/choice_parameters.html'
    form_class = forms.ChoiceEmployeeParametersForm

    def get_success_url(self):
        return reverse_lazy('team:check_employee', kwargs={'company_id': self.kwargs['company_id']})

    def form_valid(self, form):
        self.request.user.json_with_settings_info["settings_info_about_company_employee"] = []
        for item, flag in form.cleaned_data.items():
            if flag: self.request.user.json_with_settings_info["settings_info_about_company_employee"].append(item)
            self.request.user.save()
        return super().form_valid(form)


class CreateCategory(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('team:login')
    form_class = forms.CategoryCreationForm
    success_url = reverse_lazy('team:homepage')
    extra_context = {'title': 'QuickHub: Category-create'}
    template_name = creator

    def form_valid(self, form):
        user_proj = form.save(commit=False)
        user_proj.title = form.cleaned_data.get('title')
        user_proj.employee_id = models.Employee.objects.get(id=self.request.user.id)
        user_proj.project_personal_notes = form.cleaned_data.get('project_personal_notes')
        user_proj.save()
        return super().form_valid(user_proj)


class CreatePosition(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('team:login')
    success_url = reverse_lazy('team:homepage')
    form_class = forms.PositionCreationForm
    template_name = creator
    extra_context = {'title': 'Position: Company-create'}

    def form_valid(self, form):
        position = form.save(commit=False)
        position.company_id = self.kwargs['company_id']
        position.json_with_optional_info = {'text': form.cleaned_data.get('text')}
        position.save()
        return super().form_valid(position)


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
    return render(request, 'team/main_functionality/homepage.html')


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
        'title': 'Taskboard-create'
    }
    return render(request, creator, context)


@login_required(login_url=reverse_lazy('team:login'))
def taskboard(request):
    categories = models.UserProject.objects.filter(employee_id=request.user.id)

    cats = {}
    for cat in categories:
        cats[cat] = models.Employee.objects.get(id=request.user.id).tasks \
            .filter(id__in=models.UserProjectTask.objects.filter(user_project_id=cat).values('task_id'))

    context = {'cats': cats}
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
            department.company_id = models.Company.objects.get(id=company)
            try:
                department.parent_id = models.Department.objects \
                    .get(Q(title=form.cleaned_data.get('parent')) & Q(company_id=company))
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

    context = {'form': form}
    return render(request, 'team/main_functionality/create_department.html', context)


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
