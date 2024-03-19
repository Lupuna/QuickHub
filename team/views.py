from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, UpdateView, FormMixin
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.db.models import Count, Q, QuerySet

from . import forms, models, utils, permissions
from user_project_time import (
    models as upt_models,
    forms as upt_forms,
    utils as upt_utils,
    services as upt_services
    )
from QuickHub import utils as quickhub_utils


# ///    Employee   ///


class ChoiceParameters(FormView):
    login_url = reverse_lazy('registration:login')
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


class UserCompaniesListView(quickhub_utils.ModifiedDispatch, LoginRequiredMixin, ListView):
    model = models.Company
    template_name = 'team/main_functionality/list_views/user_companies.html'
    context_object_name = 'companies'

    def get_queryset(self):
        return self.request.user.companies.distinct()


class UserProjectsListView(LoginRequiredMixin, ListView):
    model = models.Project
    template_name = 'team/main_functionality/list_views/user_projects.html'
    context_object_name = 'projects'

    def get_queryset(self) -> QuerySet[models.Project]:
        tasks = self.request.user.tasks.select_related('project_id')
        projects_ids = tasks.values_list('project_id', flat=True)

        projects = models.Project.objects\
            .filter(id__in=projects_ids)\
            .annotate(
                tasks_count=Count('tasks'),
                ready_count=Count('tasks', filter=Q(tasks__task_status='Ready'))
            )
        return projects


class UserProfileListView(LoginRequiredMixin, ListView):
    model = models.Company
    template_name = 'team/main_functionality/list_views/user_profile.html'
    context_object_name = 'companies'
    login_url = reverse_lazy('registration:login')

    def get_queryset(self):
        return self.request.user.companies.distinct()


class UpdateUserProfile(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('registration:login')
    success_url = reverse_lazy('team:user_profile')
    model = models.Employee
    template_name = quickhub_utils.creator
    fields = ['image', 'name', 'telephone', 'email', 'city', 'birthday']
    extra_context = {'button': 'update'}
    success_message = 'Параметры успешно изменены!'

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs['pk'] != self.request.user.pk:
            return redirect(reverse_lazy('team:user_profile'))
        return super().dispatch(request, *args, **kwargs)


class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    form_class = forms.SetPasswordForm
    template_name = quickhub_utils.creator
    login_url = reverse_lazy('registration:login')
    extra_context = {'button': 'update'}
    success_url = reverse_lazy('team:user_profile')
    success_message = 'Ваш пароль был успешно изменен!'


# ///   Company   ///


class CreateCompany(quickhub_utils.CreatorMixin, LoginRequiredMixin, FormView):
    form_class = forms.CompanyCreationForm

    def form_valid(self, form):
        company = form.save(commit=False)
        company.owner_id = self.request.user.id
        company.save()
        utils.add_new_employee(company.id, self.request.user.id)
        return super().form_valid(company)


class CreatePosition(quickhub_utils.ModifiedDispatch, quickhub_utils.CreatorMixin, FormView):
    form_class = forms.PositionCreationForm

    def form_valid(self, form):
        position = form.save(commit=False)
        position.company_id = self.kwargs['company']
        position.json_with_optional_info = {'text': form.cleaned_data.get('text')}
        position.save()
        return super().form_valid(position)


class CreateCompanyEvent(quickhub_utils.ModifiedDispatch, quickhub_utils.CreatorMixin, FormView):
    form_class = forms.CompanyEventCreationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company_id'] = self.kwargs['company']
        return kwargs

    def form_valid(self, form):
        company_event = models.CompanyEvent()
        company_event.company = self.kwargs['company']
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


class CreateDepartment(quickhub_utils.ModifiedDispatch, quickhub_utils.CreatorMixin, FormView):
    form_class = forms.DepartmentCreationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company_id'] = self.kwargs['company']
        return kwargs

    def form_valid(self, form):
        department = models.Department()
        try:
            department.company_id = self.kwargs['company']
            department.title = form.cleaned_data.get('title')
            department.parent_id = form.cleaned_data.get('parent')
            department.supervisor = form.cleaned_data.get('supervisor')
            department.save()
        except IntegrityError:
            return redirect('team:create_department',
                            company_id=self.kwargs['company_id'])

        employees = list(form.cleaned_data.get('employees'))
        if department.supervisor not in employees:
            employees += [department.supervisor]


        for employee in employees:
            employee_company = models.EmployeeCompany.objects \
                .filter(employee_id=employee,
                        company_id=self.kwargs['company'])
            # т.к. on_delete=models.SET_NULL, то при удалении департамента может возникнуть много
            # записей об одном работнике с пустыми полями отдела
            employee_without_department = employee_company.filter(department_id=None)
            if employee_without_department:
                employee_without_department[0].department_id = department
                employee_without_department[0].save()
            else:
                employee_company = models.EmployeeCompany()
                employee_company.company_id = self.kwargs['company']
                employee_company.employee_id = employee
                employee_company.department_id = department
                employee_company.save()
        return super().form_valid(department)


class CheckEmployee(quickhub_utils.ModifiedDispatch, ListView):
    template_name = 'team/main_functionality/list_views/company_employees.html'
    model = models.Employee
    paginate_by = 10
    login_url = reverse_lazy('registration:login')

    def get_queryset(self):
        info_filter_about_employee = self.request.user.json_with_settings_info["settings_info_about_company_employee"]
        company = self.kwargs['company']
        # prefetch_related('links', 'positions', 'departments')
        employees = company.employees.prefetch_related('links').all()
        info_about_employees = []
        for employee in employees:
            info_about_employee = dict(
                filter(lambda x: x[0] in info_filter_about_employee, employee.get_all_info().items()))
            for link in employee.links.all():
                if link.title in info_filter_about_employee:
                    info_about_employee.update(link.get_info())

            if 'position_title' in info_filter_about_employee:
                position = employee.positions.filter(company_id=company)
                if position:
                    position = position[0].title
                else:
                    position = None
                info_about_employee.update({'position_title': position})

            if 'department' in info_filter_about_employee:
                department = employee.departments.filter(company_id=company)
                if department:
                    department = department[0].title
                else:
                    department = None
                info_about_employee.update({'department': department})

            info_about_employees.append(info_about_employee)
        return info_about_employees


class CompanyDetailView(quickhub_utils.ModifiedDispatch, DetailView):
    model = models.Company
    template_name = 'team/main_functionality/detail_views/company.html'
    context_object_name = 'company'
    pk_url_kwarg = 'company_id'

    def get_object(self):
        return self.kwargs['company']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        company = self.get_object()
        roots = company.departments.select_related('supervisor')\
                .prefetch_related('childs')\
                .filter(parent_id=None)
        context['roots'] = roots
        return context


class PositionsListView(quickhub_utils.ModifiedDispatch, ListView):
    model = models.Positions
    template_name = 'team/main_functionality/list_views/positions.html'
    context_object_name = 'positions'

    def get_queryset(self):
        return self.kwargs['company'].positions.all()


class DepartmentDetailView(DetailView):
    model = models.Department
    template_name = 'team/main_functionality/detail_views/department.html'
    context_object_name = 'department'
    pk_url_kwarg = 'department_id'

    def get_object(self):
        return models.Department.objects\
            .select_related('supervisor')\
            .get(id=self.kwargs[self.pk_url_kwarg])


class DepartmentsListView(quickhub_utils.ModifiedDispatch, ListView):
    model = models.Department
    template_name = 'team/main_functionality/list_views/departments.html'
    context_object_name = 'departments'

    def get_queryset(self):
        return self.kwargs['company'].departments.all()


# ///   Project    ///


class CreateProject(quickhub_utils.ModifiedDispatch, quickhub_utils.CreatorMixin, FormView):
    form_class = forms.ProjectCreationForm

    def form_valid(self, form):
        project = form.save(commit=False)
        project.project_creater = self.request.user.id
        project.company_id = self.kwargs['company']
        form.save()
        return super().form_valid(form)


class ProjectsListView(quickhub_utils.ModifiedDispatch, ListView):
    model = models.Project
    template_name = 'team/main_functionality/list_views/projects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return self.kwargs['company'].projects.all()


class ProjectDetailView(quickhub_utils.ModifiedDispatch, DetailView):
    model = models.Project
    template_name = 'team/main_functionality/detail_views/project.html'
    context_object_name = 'project'
    pk_url_kwarg = 'project_id'


# ///   Task    ///


class CreateTask(quickhub_utils.ModifiedDispatch, quickhub_utils.CreatorMixin, FormView):
    form_class = forms.TaskCreationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company_id'] = self.kwargs['company']
        kwargs['project_id'] = self.kwargs['project']
        return kwargs

    def form_valid(self, form):
        task = models.Task()
        task.json_with_employee_info = {
            'appoint': [self.request.user.email],
            'responsible': [i.email for i in form.cleaned_data.get('responsible')],
            'executor': [i.email for i in form.cleaned_data.get('executor')]
        }
        task.project_id = self.kwargs['project']
        task.text = form.cleaned_data.get('text')
        task.title = form.cleaned_data.get('title')
        task.save()

        self.request.user.tasks.add(task)
        self.request.user.categories.get(title='Мои задачи').tasks.add(task)
        
        upt_services.create_task_deadline(user=self.request.user, task=task)
        
        for executor in form.cleaned_data.get('executor'):
            if executor == self.request.user:
                continue
            executor.tasks.add(task)
            executor.categories.get(title='Мои задачи').tasks.add(task)
            upt_services.create_task_deadline(user=executor, task=task)

        for f in self.request.FILES.getlist('files'): models.TaskFile.objects.create(file=f, task_id=task)
        for i in self.request.FILES.getlist('images'): models.TaskImage.objects.create(image=i, task_id=task)
        return super().form_valid(task)


class CreateSubtask(quickhub_utils.ModifiedDispatch, quickhub_utils.CreatorMixin, FormView):
    form_class = forms.SubtaskCreationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company_id'] = self.kwargs['company']
        return kwargs

    def form_valid(self, form):
        subtask = models.Subtasks()
        subtask.json_with_employee_info = {
            'appoint': [self.request.user.email],
            'responsible': [i.email for i in form.cleaned_data.get('responsible')],
            'executor': [i.email for i in form.cleaned_data.get('executor')]
        }
        subtask.task_id_id = self.kwargs['task_id']
        subtask.text = form.cleaned_data.get('text')
        subtask.title = form.cleaned_data.get('title')
        subtask.save()
        for f in self.request.FILES.getlist('files'): models.SubtaskFile.objects.create(file=f, subtask_id=subtask)
        for i in self.request.FILES.getlist('images'): models.SubtaskImage.objects.create(image=i, subtask_id=subtask)
        return super().form_valid(subtask)


class TaskDetailView(quickhub_utils.ModifiedDispatch, FormMixin, DetailView):
    model = models.Task
    form_class = upt_forms.SetTaskDeadlineForm
    template_name = 'team/main_functionality/detail_views/task.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_object(self):
        return self.kwargs['task']

    def get_success_url(self):
        return reverse_lazy('team:task', kwargs={'company_id': self.kwargs['company_id'],
                                                 'project_id': self.kwargs['project_id'],
                                                 'task_id': self.kwargs['task_id']})

    def get_context_data(self, *args, **kwargs):
        context = super(TaskDetailView, self).get_context_data(*args, **kwargs)
        context['form'] = upt_forms.SetTaskDeadlineForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        self.object = self.kwargs['task']

        time_start = form.cleaned_data.get('time_start')
        time_end = form.cleaned_data.get('time_end')
        upt_services.update_deadline(
            user=self.request.user,
            task=self.object,
            start=time_start,
            end=time_end
        )

        return super(TaskDetailView, self).form_valid(form)
    
    def form_invalid(self, form):
        self.object = self.kwargs['task']
        return super(TaskDetailView, self).form_invalid(form)


class SubtaskDetailView(quickhub_utils.ModifiedDispatch, DetailView):
    model = models.Subtasks
    template_name = 'team/main_functionality/detail_views/subtask.html'
    context_object_name = 'subtask'
    pk_url_kwarg = 'subtask_id'


# ///   Else    ///


@login_required(login_url=reverse_lazy('registration:login'))
def homepage(request):
    return render(request, 'team/main_functionality/homepage.html')
