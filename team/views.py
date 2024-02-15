from typing import Any
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.forms import BaseForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from . import forms, models, utils


class CreateCompany(utils.CreatorMixin, LoginRequiredMixin, FormView):
    form_class = forms.CompanyCreationForm

    def form_valid(self, form):
        company = form.save(commit=False)
        company.owner_id = self.request.user.id
        company.save()
        utils.add_new_employee(company.id, self.request.user.id)
        return super().form_valid(company)


class CreateProject(utils.CreatorMixin, LoginRequiredMixin, utils.ModifiedFormView):
    form_class = forms.ProjectCreationForm

    def form_valid(self, form):
        project = form.save(commit=False)
        project.project_creater = self.request.user.id
        project.company_id = self.kwargs['company_id']
        form.save()
        return super().form_valid(form)


class CreateTask(utils.CreatorMixin, LoginRequiredMixin, utils.ModifiedFormView):
    form_class = forms.TaskCreationForm

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


class CreateSubtask(utils.CreatorMixin, LoginRequiredMixin, utils.ModifiedFormView):
    form_class = forms.SubtaskCreationForm

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


class CreateCategory(utils.CreatorMixin, LoginRequiredMixin, FormView):
    form_class = forms.CategoryCreationForm

    def form_valid(self, form):
        try:
            category = form.save(commit=False)
            category.title = form.cleaned_data.get('title')
            category.employee_id = models.Employee.objects.get(id=self.request.user.id)
            category.project_personal_notes = form.cleaned_data.get('project_personal_notes')
            category.save()
        except:
            self.extra_context.update({
                'error': f'Категория {category.title} уже создана'
            })
            return redirect(reverse_lazy('team:create_category'))
        return super().form_valid(category)


class CreatePosition(utils.CreatorMixin, LoginRequiredMixin, utils.ModifiedFormView):
    form_class = forms.PositionCreationForm

    def form_valid(self, form):
        position = form.save(commit=False)
        position.company_id = self.kwargs['company_id']
        position.json_with_optional_info = {'text': form.cleaned_data.get('text')}
        position.save()
        return super().form_valid(position)


class CreateDepartment(utils.CreatorMixin, LoginRequiredMixin, utils.ModifiedFormView):
    form_class = forms.DepartmentCreationForm

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['company_id'] = self.kwargs['company_id']
        return kwargs

    def form_valid(self, form):
        department = models.Department()
        try:
            department.title = form.cleaned_data.get('title')
            department.company_id = self.kwargs['company_id']

            department.parent_id = form.cleaned_data.get('parent')
            department.supervisor = form.cleaned_data.get('supervisor')
            department.save()

            employees = list(form.cleaned_data.get('employees'))
            if not department.supervisor in employees:
                employees += [department.supervisor]

            for employee in employees:
                employee_company = models.EmployeeCompany.objects\
                    .filter(employee_id=employee, 
                            company_id=self.kwargs['company_id'])
                # т.к. on_delete=models.SET_NULL, то при удалении департамента может возникнуть много
                # записей об одном работнике с пустыми полями отдела 
                employee_without_department = employee_company.filter(department_id=None)
                if employee_without_department:
                    employee_without_department[0].department_id = department     # если есть запись о работнике с незаполненным полем отдела,
                    employee_without_department[0].save()                         # тогда просто заполняется поле отдела в уже существующей записи
                else:
                    employee_company = models.EmployeeCompany()
                    employee_company.company_id = self.kwargs['company_id']
                    employee_company.employee_id = employee
                    employee_company.department_id = department     # если же во всех записях работник уже прикреплён к отделу, 
                    employee_company.save()                         # создаётся новая запись в таблице EmployeeCompany
        except Exception as ex:
            print(ex)
            self.extra_context.update({
                'error': f'{department.title} уже существует'
            })
            return redirect('team:create_department', 
                            company_id=self.kwargs['company_id'].id)
        return super().form_valid(department)


class CreateTaskboard(utils.CreatorMixin, LoginRequiredMixin, utils.ModifiedFormView):
    form_class = forms.TaskboardCreationForm
    
    def dispatch(self, request, *args, **kwargs):
        try:
            self.kwargs['user'] = models.Employee.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
            return redirect(reverse_lazy('team:homepage'))
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['emp_id'] = self.kwargs['user'].id
        return kwargs

    def form_valid(self, form: Any) -> HttpResponse:
        tasks = self.kwargs['user'].tasks\
            .filter(id__in=form.cleaned_data.get('tasks'))
        category = form.cleaned_data.get('category')
        
        for task in tasks:
            taskboard = models.Taskboard(category_id=category,
                                        task_id=task,
                                        title=category.title,
                                        task_personal_notes={
                                            'notes': form.cleaned_data.get('text'),
                                            'task_notes': task.text
                                        })
            subtasks = task.subtasks.all()
            for subtask in subtasks:
                taskboard.json_with_subtask_and_subtask_personal_note[subtask.id] = subtask.text
            taskboard.save()
        return super().form_valid(form)


def sign_up(request):
    if request.method == 'POST':
        form = forms.CustomUserCreationFrom(request.POST)
        if form.is_valid():
            user = form.save()
            user.json_with_settings_info = utils.create_base_settings_json_to_employee()
            user.save()
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
def taskboard(request):
    categories = models.Category.objects.filter(employee_id=request.user.id)
    emlpoyee = models.Employee.objects.get(id=request.user.id)
    cats = {}
    for cat in categories:
        taskboards = models.Taskboard.objects.filter(category_id=cat)
        cats[cat] = emlpoyee.tasks.filter(id__in=taskboards.values('task_id'))

    context = {'cats': cats}
    return render(request, 'team/main_functionality/taskboard.html', context)


@login_required(login_url=reverse_lazy('team:homepage'))
def view_department(request, company_id, department_id):
    department = models.Department.objects.get(id=department_id, company_id=company_id)
    supervisor = models.Employee.objects.get(id=department.supervisor.id)
    employees = models.Employee.objects \
        .filter(id__in=models.EmployeeCompany.objects \
                .filter(department_id=department_id, company_id=company_id).values('employee_id'))

    context = {
        'department': department,
        'employees': employees,
        'supervisor': supervisor,
    }
    return render(request, 'team/main_functionality/view_department.html', context)


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
