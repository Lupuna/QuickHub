from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import IntegrityError
from . import forms, models, utils, permissions


class CreateCompany(utils.CreatorMixin, LoginRequiredMixin, FormView):
    form_class = forms.CompanyCreationForm

    def form_valid(self, form):
        company = form.save(commit=False)
        company.owner_id = self.request.user.id
        company.save()
        utils.add_new_employee(company.id, self.request.user.id)
        return super().form_valid(company)


class CreateProject(utils.CreatorMixin, permissions.CompanyAccess, utils.ModifiedFormView):
    form_class = forms.ProjectCreationForm

    def form_valid(self, form):
        project = form.save(commit=False)
        project.project_creater = self.request.user.id
        project.company_id = self.kwargs['company_id']
        form.save()
        return super().form_valid(form)


class CreateTask(utils.CreatorMixin, permissions.CompanyAccess, utils.ModifiedFormView):
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


class CreateSubtask(utils.CreatorMixin, permissions.CompanyAccess, utils.ModifiedFormView):
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


class ChoiceParameters(permissions.CompanyAccess, FormView):
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
            return redirect(reverse_lazy('team:create_category'))
        return super().form_valid(category)


class CreatePosition(utils.CreatorMixin, permissions.CompanyAccess, utils.ModifiedFormView):
    form_class = forms.PositionCreationForm

    def form_valid(self, form):
        position = form.save(commit=False)
        position.company_id = self.kwargs['company_id']
        position.json_with_optional_info = {'text': form.cleaned_data.get('text')}
        position.save()
        return super().form_valid(position)


class CreateCompanyEvent(utils.CreatorMixin, permissions.CompanyAccess, utils.ModifiedFormView):
    form_class = forms.CompanyEventCreationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company_id'] = self.kwargs['company_id']
        return kwargs

    def form_valid(self, form):
        company_event = models.CompanyEvent()
        company_event.company = self.kwargs['company_id']
        company_event.title = form.cleaned_data.get('title')
        company_event.description = form.cleaned_data.get('description')
        company_event.json_with_employee_info = {
            'present_employees': [employee.email for employee in form.cleaned_data.get('present_employees')]
        }
        company_event.time_end = form.cleaned_data.get('time_end')
        company_event.time_start = form.cleaned_data.get('time_start')
        company_event.save()

        for f in self.request.FILES.getlist('files'): models.CompanyEventFile.objects.create(file=f,
                                                                                             company_event=company_event)
        for i in self.request.FILES.getlist('images'): models.CompanyEventImage.objects.create(image=i,
                                                                                               company_event=company_event)

        return super().form_valid(form)


class CreateDepartment(utils.CreatorMixin, permissions.CompanyAccess, utils.ModifiedFormView):
    form_class = forms.DepartmentCreationForm

    def get_form_kwargs(self):
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
        except IntegrityError:
            return redirect('team:create_department',
                            company_id=self.kwargs['company_id'].id)

        employees = list(form.cleaned_data.get('employees'))
        if not department.supervisor in employees:
            employees += [department.supervisor]

        for employee in employees:
            employee_company = models.EmployeeCompany.objects \
                .filter(employee_id=employee,
                        company_id=self.kwargs['company_id'])
            # т.к. on_delete=models.SET_NULL, то при удалении департамента может возникнуть много
            # записей об одном работнике с пустыми полями отдела
            employee_without_department = employee_company.filter(department_id=None)
            if employee_without_department:
                employee_without_department[0].department_id = department  # если есть запись о работнике с незаполненным полем отдела,
                employee_without_department[0].save()  # тогда просто заполняется поле отдела в уже существующей записи
            else:
                employee_company = models.EmployeeCompany()
                employee_company.company_id = self.kwargs['company_id']
                employee_company.employee_id = employee
                employee_company.department_id = department     # если же во всех записях работник уже прикреплён к отделу, 
                employee_company.save()                         # создаётся новая запись в таблице EmployeeCompany
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

    def form_valid(self, form):
        tasks = self.kwargs['user'].tasks \
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

'''Классы отображений'''

class CheckEmployee(permissions.CompanyAccess, utils.ModifiedListView):
    template_name = 'team/main_functionality/view_company_employees.html'
    context_object_name = 'page_obj'
    model = models.Employee
    login_url = reverse_lazy('team:login')

    def get_queryset(self):
        info_filter_about_employee = self.request.user.json_with_settings_info["settings_info_about_company_employee"]
        # employees = models.Employee.objects.filter(
        #     id__in=models.EmployeeCompany.objects.filter(company_id=self.kwargs['company_id']).values('employee_id'))
        company = self.kwargs['company_id']
        employees = company.employees.all()

        info_about_employees = []
        for employee in employees:
            info_about_employee = dict(
                filter(lambda x: x[0] in info_filter_about_employee, employee.get_all_info().items()))
            for link in employee.links.all():
                if link.title in info_filter_about_employee:
                    info_about_employee.update(link.get_info())

            if 'position_title' in info_filter_about_employee:
                # position = models.Positions.objects.filter(
                #     id__in=models.EmployeeCompany.objects.filter(Q(employee_id=employee.id) & Q(company_id= self.kwargs['company_id'])))
                position = employee.positions.filter(company_id=company)
                if position:
                    position = position[0].title
                else:
                    position = None
                info_about_employee.update({'position_title': position})

            if 'department' in info_filter_about_employee:
                # department = models.Department.objects.filter(
                #     id__in=models.EmployeeCompany.objects.filter(Q(employee_id=employee.id) & Q(company_id=self.kwargs['company_id']))
                # )
                department = employee.departments.filter(company_id=company)
                if department:
                    department = department[0].title
                else:
                    department = None
                info_about_employee.update({'department': department})

            info_about_employees.append(info_about_employee)

        # paginator = Paginator(info_about_employees, 1)
        # page_number = self.request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        return info_about_employees


class TaskboardListView(LoginRequiredMixin, ListView):
    model = models.Employee
    template_name = 'team/main_functionality/taskboard.html'


class ProjectsListView(permissions.CompanyAccess, utils.ModifiedListView):
    model = models.Project
    template_name = 'team/main_functionality/projects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return self.kwargs['company_id'].projects.all()


class DepartmentsListView(permissions.CompanyAccess, utils.ModifiedListView):
    model = models.Department
    template_name = 'team/main_functionality/departments.html'
    context_object_name = 'departments'

    def get_queryset(self):
        return self.kwargs['company_id'].departments.all()


class PositionsListView(permissions.CompanyAccess, utils.ModifiedListView):
    model = models.Positions
    template_name = 'team/main_functionality/view_positions.html'
    context_object_name = 'positions'
    
    def get_queryset(self):
        return self.kwargs['company_id'].positions.all()


class DepartmentDetailView(permissions.CompanyAccess, DetailView):
    model = models.Department
    template_name = 'team/main_functionality/view_department.html'
    context_object_name = 'department'
    pk_url_kwarg = 'department_id'

    def get_queryset(self):
        return super().get_queryset().filter(company_id=self.kwargs['company_id'])


class TaskDetailView(permissions.CompanyAccess, DetailView):
    model = models.Task
    template_name = 'team/main_functionality/view_task.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get(self, request, *args, **kwargs):
        try:
            return super(TaskDetailView, self).get(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return redirect(reverse_lazy('team:taskboard'))

    def get_object(self, queryset=None):
        project = models.Project.objects.get(id=self.kwargs['project_id'], 
                                            company_id=self.kwargs['company_id'])
        return project.tasks.get(id=self.kwargs[self.pk_url_kwarg])
    

class SubtaskDetailView(permissions.CompanyAccess, DetailView):
    model = models.Subtasks
    template_name = 'team/main_functionality/view_subtask.html'
    context_object_name = 'subtask'
    pk_url_kwarg = 'subtask_id'

    def get(self, request, *args, **kwargs):
        try:
            return super(SubtaskDetailView, self).get(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return redirect(reverse_lazy('team:taskboard'))

    def get_object(self, queryset=None):
        task = models.Task.objects.get(id=self.kwargs['task_id'],
                                       project_id=self.kwargs['project_id'], 
                                        project_id__company_id=self.kwargs['company_id'])
        return task.subtasks.get(id=self.kwargs[self.pk_url_kwarg])


class ProjectDetailView(permissions.CompanyAccess, DetailView):
    model = models.Project
    template_name = 'team/main_functionality/view_project.html'
    context_object_name = 'project'
    pk_url_kwarg = 'project_id'

    def get(self, request, *args, **kwargs):
        try:
            return super(ProjectDetailView, self).get(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return redirect(reverse_lazy('team:taskboard'))

    def get_queryset(self):
        return super().get_queryset().filter(company_id=self.kwargs['company_id'])


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