from django.forms import BaseModelForm
from django.shortcuts import render
from .models import Course

class Assignment:
    def __init__(self, id):
        self.id = id

class Courses:
    def __init__(self, name, code, credits):
        self.name = name
        self.code = code
        self.credits = credits
        self.assignemts = []

    def display_info(self):
        print(f"Course Name: {self.name}")
        print(f"Course Code: {self.code}")
        print(f"Course Credits: {self.credits}")

def home(request):
    context = {
        'courses': Course.objects.all()
    }
    return render(request,'assignment/home.html',context)

def assignment(request):
    return render(request,'assignment/assignments.html')

def homepage(request):
    context={
        'name': "Siddhant !",
        'course1' : Courses("Fundamental Comp Sci","CS101",10),
        'course2' : Courses("Biology","BT001",6)
    }

    return render(request, "assignment/" , context)


    
 

def assignments(req):
    ass1 = Assignment(1)
    ass2 = Assignment(2)
    ass3 = Assignment(3)

    assignments = [ass1 , ass2 , ass3 ]

    return render(req, "tas/assignment.html" , { 'assignments' : assignments })





