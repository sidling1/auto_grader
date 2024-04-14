# This is a assignment submission software which integrates plag checker and auto grader tools

# To Run

git clone the repo
python3 manage.py makemigrations assignment tas
python3 manage.py migrate
python3 manage.py runserver

# Temporary credentials for instructor
username : avinav
password : pass@123

# Features

1. Instructor side login
2. Student side login
3. Add submissions for an assignment
4. Remove submission for an assignment
3. Plag checker for the instructor
5. Plag checker shows clearly where the match was found
6. Secure file uploads to the database in various formats
7. Assignments have due dates to ensure on time submission
8. Auto grader for the instructor
9. Assesses coding practice and quality for the auto grader

# To add
1. Interface for instructors to review submissions and leave comments (added the backend)
2. Interface for students to review submissiobs

# Known Bugs
1. The student login system has a bug that does not allow it to login right now
2. Auto grading system cannot access file