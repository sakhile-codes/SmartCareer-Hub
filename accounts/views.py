from .models import CustomUser
from django import forms

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        user, created = CustomUser.objects.get_or_create(phone_number=phone_number)
        if created:
            login(request, user)
            return redirect('login')  # Redirect to a home page or dashboard
        else:
            messages.error(request, 'Phone number already registered.')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            login(request, user)
            return redirect('home')  # Redirect to a home page or dashboard
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid phone number.')
    return render(request, 'login.html')

@login_required
def home_view(request):
    return render(request, 'home.html')
