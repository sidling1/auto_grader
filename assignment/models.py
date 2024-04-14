from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/assignment_<id>/filename
    return f"user_{instance.student.id}/assignment_{instance.assignment.id}/{filename}"


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.code

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return self.title
    
class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE,null=True)
    submission_details = models.TextField()
    grades = models.FloatField(null=True, blank=True)
    code_file = models.FileField(upload_to=user_directory_path, null=True, blank=True)

    def __str__(self):
        return str(self.id)



