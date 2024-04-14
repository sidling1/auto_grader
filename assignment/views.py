from django.forms import BaseModelForm
from django.shortcuts import render,get_object_or_404,redirect
from .models import Course,Assignment,Submission
from django.contrib.auth.models import User
from .forms import SubmissionForm

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
    if request.method=="POST":
        username =request.user.username
        user = User.objects.get(username=username)
        course = get_object_or_404(Course, code=course_id)
        assignment = Assignment.objects.get(id=assignment_id)
        submission_details = "Submitted on time"
        grades="0.0"
        code_file = request.FILES.get('input_file')
        # try to get the submission made by this user
        submission = Submission(student=user, assignment=assignment,submission_details=submission_details,grades=grades,code_file=code_file)
        try:
            submission.save()
        except InterruptedError:
            return redirect('home')
        return redirect('submission', course_id = course_id,assignment_id=assignment_id)

    
    username =request.user.username
    user = User.objects.get(username=username)
    course = get_object_or_404(Course, code=course_id)
    assignment = Assignment.objects.get(id=assignment_id)
    # try to get the submission made by this user
    submission = Submission.objects.filter(student=user, assignment_id=assignment_id).first()
    print(submission)
    # print(assignment)
    context={
        'user':user,
        'course':course,
        'assignment':assignment,
        'submission':submission
    }
    
    return render(request,'assignment/submit_assignment.html',context)


def remove_submission(request,submission_id):

    submission = get_object_or_404(Submission, pk=submission_id)
    assignment_id = submission.assignment.id
    course_code = submission.assignment.course.code
    
    submission.delete()
    return redirect('submission',course_id=course_code, assignment_id=assignment_id)



    
 






