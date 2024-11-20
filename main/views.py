from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

# Create your views here.
def main(request):
    return render(request, "mainv2.html", {})