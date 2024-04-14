from django.shortcuts import render,redirect
from assignment.models import Course,Assignment,Submission,TAs
from .forms import AddCourse,AddAssignment
from django.db import IntegrityError
from django.contrib.auth import logout

# Create your views here.
def home(req):
    return render(req, "tas/home.html")

def homepage(req):
    name = req.user.username

    ta =  TAs.objects.filter(ta=req.user)

    if ta.exists() == False:
        print('Not a TA')
        logout(req)
        return redirect('login')

    ta = ta.first()
    courses = ta.courses.all()

    return render(req, "tas/homepage.html" , {'name':name , 'courses' : courses})

def course(req, course_code):
    name = req.user.username

    
    course = Course.objects.get(code=course_code)
    assignments = Assignment.objects.filter(course=course)

    return render(req, "tas/course.html" , { 'assignments' : assignments , 'name' : name , 'course' : course_code })

def submissions(req, course_code, ass_id):

    ass = Assignment.objects.get(id=ass_id)
    # TODO : Add feature that allows TAs to See the submissions
    submissions = Submission.objects.filter(assignment=ass)

    return render(req, "tas/submissions.html" , {'submissions':submissions , 'course_code' : course_code , 'ass_id' : ass_id})

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

                ta = TAs.objects.get(ta=req.user)
                ta.courses.add(course)
                ta.save()
                # If execution reaches here, it means the object was saved successfully
                return redirect('home')
            except IntegrityError:
                # Handle the case where the object could not be saved due to integrity constraint violation
                return redirect('home')
    else:
        form = AddCourse() 

    return render(req, "tas/addCourse.html" , {'form':form})

def addStudents(req):
    # TODO : Implement this feature later that allows the TA to select students to enroll into the course
    # TODO : Also can Implement a feature to add various TAs to the same course / or maybe every TA can use the same id for now lol
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
                return redirect('course',course_code)
            except IntegrityError:
                # Handle the case where the object could not be saved due to integrity constraint violation
                return redirect('course',course_code)
    else:
        form = AddAssignment() 

    return render(req, "tas/addAssignment.html", {'form' : form })


def autograder(req, course_code, ass_id):
    
    # TODO : Use the autograder script to auto grade each submission
    return render(req, "tas/autograder.html")

def plagcheck(req, course_code, ass_id):

    # TODO : Use the plagchecker script to plagiarise each submission
    return render(req, "tas/plaqchecker.html")

def manualgrader(req, course_code, ass_id, sub_id):

    return render(req, "tas/manualgrader.html")