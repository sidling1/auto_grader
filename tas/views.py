from django.shortcuts import render,redirect
from assignment.models import Course,Assignment
from .forms import AddCourse,AddAssignment
from django.db import IntegrityError

# Create your views here.
def home(req):
    return render(req, "tas/home.html")

def homepage(req):
    name = "Siddhant !"

    courses = Course.objects.all()
    return render(req, "tas/homepage.html" , {'name':name , 'courses' : courses})

def course(req, course_code):
    name = "Siddhant"
    course = Course.objects.get(code=course_code)
    assignments = Assignment.objects.filter(course=course)

    return render(req, "tas/course.html" , { 'assignments' : assignments , 'name' : name , 'course' : course_code })

def submissions(req, course_code, ass_id):

    return render(req, "tas/submissions.html")

def addCourse(req):
    if req.method == 'POST':
        req.method = 'GET'
        form = AddCourse(req.POST)
        if form.is_valid():
            # Process form data
            name = form.cleaned_data['name']
            code = form.cleaned_data['code']
            
            # Perform actions with form data (e.g., save to database)
            try:
            # Create an instance of MyModel and save it
                course = Course(name=name,code=code)
                course.save()
                # If execution reaches here, it means the object was saved successfully
                return redirect('addcourse')
            except IntegrityError:
                # Handle the case where the object could not be saved due to integrity constraint violation
                return redirect('addcourse')
    else:
        form = AddCourse() 

    return render(req, "tas/addCourse.html" , {'form':form})

def addStudents(req):

    return render(req, "tas/addStudent.html")

def addAssignments(req, course_code):
    if req.method == 'POST':
        form = AddAssignment(req.POST)
        if form.is_valid():
            # Process form data
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            due_date = form.cleaned_data['due_date']

            # Perform actions with form data (e.g., save to database)
            try:
            # Create an instance of MyModel and save it
                course = Course.objects.get(code=course_code)
                ass = Assignment(course=course,title=title,description=description,due_date=due_date)
                
                ass.save()

                # If execution reaches here, it means the object was saved successfully
                return redirect('addassignment',course_code)
            except IntegrityError:
                # Handle the case where the object could not be saved due to integrity constraint violation
                return redirect('addassignment',course_code)
    else:
        form = AddAssignment() 

    return render(req, "tas/addAssignment.html", {'form' : form })