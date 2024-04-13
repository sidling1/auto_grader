from django.shortcuts import render


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

class Assignment:
    def __init__(self, id):
        self.id = id

    
 

# Create your views here.
def home(req):
    return render(req, "tas/home.html")

def homepage(req):
    name = "Siddhant !"
    course1 = Courses("Fundamental Comp Sci","CS101",10)
    course2 = Courses("Biology","BT001",6)

    courses = [course1,course2]
    return render(req, "tas/homepage.html" , {'name':name , 'courses' : courses})

def assignments(req):
    name = "Siddhant"
    ass1 = Assignment(1)
    ass2 = Assignment(2)
    ass3 = Assignment(3)

    assignments = [ass1 , ass2 , ass3 ]

    return render(req, "tas/course.html" , { 'assignments' : assignments , 'name' : name })

def submissions(req):

    return render(req, "tas/submissions.html")

def addCourse(req):

    return render(req, "tas/addCourse.html")

def addStudents(req):

    return render(req, "tas/addStudent.html")