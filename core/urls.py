from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'), 
    path('logout/', views.user_logout, name='user_logout'),

    # Student URLs
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),

    # Course URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/edit/<int:pk>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:pk>/', views.delete_course, name='delete_course'),

    # College URLs
    path('colleges/', views.college_list, name='college_list'),
    path('colleges/add/', views.add_college, name='add_college'),
    path('colleges/edit/<int:pk>/', views.edit_college, name='edit_college'),
    path('colleges/delete/<int:pk>/', views.delete_college, name='delete_college'),

    # Admission URLs
    path('admissions/', views.admission_list, name='admission_list'),
    path('admissions/add/', views.add_admission, name='add_admission'),
    path('admissions/edit/<int:pk>/', views.edit_admission, name='edit_admission'),
    path('admissions/delete/<int:pk>/', views.delete_admission, name='delete_admission'),
]
