from django.shortcuts import render,redirect
from assignment.models import Course,Assignment,Submission,TAs
from .forms import AddCourse,AddAssignment
from django.db import IntegrityError
from django.contrib.auth import logout
import difflib
from django.conf import settings
import io
import sys
import ast
import subprocess


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
    
    ass = Assignment.objects.get(id=ass_id)
    submissions = Submission.objects.filter(assignment=ass)
    files = [ settings.MEDIA_ROOT + '/' + sub.code_file.name for sub in submissions.all()]

    ret = grade_code(file_path=files[2])

    # TODO : Use the autograder script to auto grade each submission
    return render(req, "tas/autograder.html" , {'value' : ret})

def plagcheck(req, course_code, ass_id):

    ass = Assignment.objects.get(id=ass_id)
    submissions = Submission.objects.filter(assignment=ass)
    files = [ settings.MEDIA_ROOT + '/' + sub.code_file.name for sub in submissions.all()]

    (ret,val) = compare_files(files[0],files[1])

    # TODO : Use the plagchecker script to plagiarise each submission
    return render(req, "tas/plaqchecker.html" , {'value' : ret , 'percentage' : val})

def manualgrader(req, course_code, ass_id, sub_id):

    return render(req, "tas/manualgrader.html")


############ PLAG CHECKER ##################################

def preprocess_line(line):
    # Remove spaces, convert to lowercase, and ignore tab spacing
    return line.replace(' ', '').lower().replace('\t', '')

def compare_files(file1, file2):
    ret = ""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = f1.readlines()
        content2 = f2.readlines()

    # Preprocess lines
    content1 = [preprocess_line(line) for line in content1]
    content2 = [preprocess_line(line) for line in content2]

    # Compare the files using difflib
    diff = difflib.ndiff(content1, content2)

    matching_lines = 0
    neg_lines = 0
    for line in diff:
        if line.startswith('  '):
            print(line)
            ret += line
            ret += '\n'
            matching_lines += 1
        elif line.startswith('- '):
            neg_lines += 1

    # Calculate plagiarism percentage
    total_lines = len(content1)
    plagiarism_percentage = (matching_lines / total_lines) * 100

    print(f'The files {file1} and {file2} are {plagiarism_percentage}% plagiarized.')
    ret += '\n\n'
    ret += f'The files {file1} and {file2} are {plagiarism_percentage}% plagiarized.'

    return (ret,plagiarism_percentage)
#################### auto grader #######################################


def grade_code(file_path):
    ret = []
    try:
        with open(file_path, 'r') as file:
            submitted_code = file.read()

        sys.stdout = io.StringIO()
        parsed_code = ast.parse(submitted_code)
        code_obj = compile(parsed_code, "<string>", "exec")
        exec(code_obj)
        output = sys.stdout.getvalue()
        sys.stdout = sys.__stdout__

        # Coding style assessment using pycodestyle
        pycodestyle_result = subprocess.run(["pycodestyle", file_path], capture_output=True, text=True)
        if pycodestyle_result.returncode != 0:
            ret.append("Coding Style Error:\n" + pycodestyle_result.stderr)
            print("Coding Style Error:\n" + pycodestyle_result.stderr)

        # Documentation quality assessment using pydocstyle
        pydocstyle_result = subprocess.run(["pydocstyle", file_path], capture_output=True, text=True)
        if pydocstyle_result.returncode != 0:
            ret.append("Documentation Quality Error:\n" + pydocstyle_result.stderr)
            print("Documentation Quality Error:\n" + pydocstyle_result.stderr)

        ret.append(f"Code executed successfully. Output: {output}")
        print(f"Code executed successfully. Output: {output}")
    except FileNotFoundError as e:
        sys.stdout = sys.__stdout__
        return f"Error: File not found: {e}"
    except SyntaxError as e:
        sys.stdout = sys.__stdout__
        return f"Syntax Error: {e}"
    except Exception as e:
        sys.stdout = sys.__stdout__
        return f"Error executing code: {e}"
    
    return ret