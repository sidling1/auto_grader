from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<course_id>/assignments/', views.course_assignments, name='course_assignments'),
    path('<course_id>/assignments/<assignment_id>', views.submission, name='submission'),
    path('submission/remove/<int:submission_id>/', views.remove_submission, name='remove_submission'),
    # path('course_id>/assignments/<assignment_id>/submit/', views.add_submission, name='add_submission'),
]