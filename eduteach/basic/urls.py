from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-course/', views.create_course, name='create-course'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register_teacher/', views.register_page_teacher, name='register_teacher'),
    path('register_student/', views.register_page_student, name='register_student'),
    path('approve_teacher/<str:pk>/', views.approve_teacher, name='approve_teacher'),
    path('reject_teacherr/<str:pk>/', views.reject_teacher, name='reject_teacher'),
    path('enroll_course/<str:pk>/', views.enroll_course, name='enroll_course'),
    path('approvals/', views.approvals, name='approvals'),
    path('all_courses/', views.all_courses, name='all_courses'),
]