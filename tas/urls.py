from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('homepage', views.homepage, name='homepage'),
    path('course/<course_code>', views.course, name='course'),
    path('submission/<course_code>/<ass_id>',views.submissions,name='submissions'),
    path('addcourse',views.addCourse, name='addcourse'),
    path('addstudent',views.addStudents, name='addstudent'),
    path('addassignment/<course_code>',views.addAssignments,name='addassignment'),
]
