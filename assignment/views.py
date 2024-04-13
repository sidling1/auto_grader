from django.forms import BaseModelForm
from django.shortcuts import render,get_object_or_404
from .models import Course,Assignment

def home(request):
    username = request.user.username
    print(username)
    context = {
        'courses': Course.objects.all(),
        'username':username
    }
    return render(request,'assignment/home.html',context)

def course_assignments(request, course_id):
    course = get_object_or_404(Course, code=course_id)
    assignments = Assignment.objects.filter(course=course)
    print("Course ID:", course.id)
    print("Course Name:", course.name)
    return render(request, 'assignment/assignments.html', {'course':course, 'assignments': assignments})

def submission(request,course_id,assignment_id):
    user =request.user.username
    course = get_object_or_404(Course, code=course_id)
    assignment = Assignment.objects.get(id=assignment_id)
    print(assignment)
    context={
        'user':user,
        'course':course,
        'assignment':assignment
    }
    
    return render(request,'assignment/submit_assignment.html',context)



    
 






