from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('homepage', views.homepage, name='home'),
    path('course/<course_code>', views.course, name='course'),
    path('submission/<course_code>/<ass_id>',views.submissions,name='submissions'),
    path('addcourse',views.addCourse, name='addcourse'),
    path('addstudent',views.addStudents, name='addstudent'),
    path('addassignment/<course_code>',views.addAssignments,name='addassignment'),
    path('login',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('autograder/<course_code>/<ass_id>',views.autograder,name='autograder'),
    path('manualgrader/<course_code>/<ass_id>/<sub_id>',views.manualgrader, name='manualgrader'),
    path('plagcheck/<course_code>/<ass_id>',views.plagcheck,name='plagcheck'),
]
