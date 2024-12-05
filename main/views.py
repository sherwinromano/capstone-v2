from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

def login_view(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

@login_required
def main_view(request):
    return render(request, 'mainv2.html')