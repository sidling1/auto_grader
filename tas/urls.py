from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('homepage', views.homepage, name='homepage'),
    path('course', views.assignments, name='assignments'),
    path('submission',views.submissions,name='submissions'),
    path('addcourse',views.addCourse, name='addcourse'),
    path('addstudent',views.addStudents, name='addstudent'),
]
