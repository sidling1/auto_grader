from django.forms import BaseModelForm
from django.shortcuts import render

def home(request):
    return render(request,'assignment/home.html')
