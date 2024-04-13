from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/assignment/<int:pk>/',views.assignment,name='assignment')
]
