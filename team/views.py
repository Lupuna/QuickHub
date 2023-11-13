from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django .contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from . import forms


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


def homepage(request):
    return render(request, 'team/main_functionality/homepage.html')
