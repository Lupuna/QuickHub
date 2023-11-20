from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django .contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
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


def add_new_employee(company_id, employee_id):
    company_id = models.Company.objects.get(id=company_id)
    employee_id = models.Employee.objects.get(id=employee_id)
    new_employee = models.EmployeeCompany(company_id=company_id, employee_id=employee_id)
    new_employee.save()
