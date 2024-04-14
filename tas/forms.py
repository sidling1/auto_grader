# forms.py
from django import forms

class AddCourse(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    code = forms.CharField(label='Code', max_length=100)

class AddStudent(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    roll_no = forms.CharField(label='Roll-Number',max_length=100)

class AddAssignment(forms.Form):
    title = forms.CharField(label='Title',max_length=100)
    description = forms.CharField(label='Description',max_length=200)
    due_date = forms.DateField(label='Due Date')