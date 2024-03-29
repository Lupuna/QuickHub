from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django .contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from . import forms, models


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
def create_company(request):
    if request.method == 'POST':
        form = forms.CompanyCreationForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner_id = request.user.id
            company.save()
            add_new_employee(company.id, request.user.id)
            return redirect(reverse_lazy('team:homepage'))
    else:
        form = forms.CompanyCreationForm()

    context = {'form': form}
    return render(request, 'team/main_functionality/create_company.html', context)


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

    context = {'form': form}
    return render(request, 'team/main_functionality/create_project.html', context)


@login_required(login_url=reverse_lazy('team:login'))
def create_task(request, company_id, project_id):
    try:
        company_id = models.Company.objects.get(id=company_id)
        project_id = models.Project.objects.get(id=project_id)
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
            for f in request.FILES.getlist('files'): models.TaskFile.objects.create(file=f, task_id=task)
            for i in request.FILES.getlist('images'): models.TaskImage.objects.create(image=i, task_id=task)
            return redirect(reverse_lazy('team:homepage'))
    else:
        form = forms.TaskCreationForm(company_id, project_id.id)

    context = {'form': form}
    return render(request, 'team/main_functionality/create_task.html', context)


def add_new_employee(company_id, employee_id):
    company_id = models.Company.objects.get(id=company_id)
    employee_id = models.Employee.objects.get(id=employee_id)
    new_employee = models.EmployeeCompany(company_id=company_id, employee_id=employee_id)
    new_employee.save()
