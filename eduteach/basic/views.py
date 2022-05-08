from multiprocessing import context
from django.shortcuts import redirect, render
from .forms import CourseForm, TeacherSignUpForm, StudentSignUpForm
from .models import User, Course, Teacher, Student
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Sum



def home(request):
    users=User.objects.all().filter(is_active=False, is_teacher=True)
    courses_created = Course.objects.all().filter(created_by=request.user.id)
    courses_enrolled = Course.objects.filter(student__user__id=request.user.id)  
    courses = Course.objects.all()
    context = {"users":users, "courses_created":courses_created, "courses":courses, 'courses_enrolled':courses_enrolled}
    return render(request, 'home.html', context)


@login_required(login_url='login')
def create_course(request):
    form=CourseForm()
    context = {'form':form}
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            Course.objects.create(created_by=request.user, name=request.POST.get('name'), description=request.POST.get('description'))
            return redirect('home')
    return render(request, 'project_form.html', context)


def register_page_teacher(request):
    form=TeacherSignUpForm()
    context = {'form':form}
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.username = user.username.lower()
            user.save()
            login(request,user)
            messages.info(request, 'Please wait for approval of admin')
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'login_register.html', context)



def register_page_student(request):
    form=StudentSignUpForm()
    context = {'form':form}
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'login_register.html', context)



def login_page(request):
    page = 'login'
    context ={'page':page}
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'User name or password does not exist')
    return render(request, 'login_register.html', context)



@login_required(login_url='login')
def approve_teacher(request, pk):
    teacher = User.objects.get(id=pk)
    teacher.is_active = True
    teacher.save()
    return redirect('home')



@login_required(login_url='login')
def reject_teacher(request, pk):
    teacher = User.objects.get(id=pk)
    teacher.delete()
    return redirect('home')



@login_required(login_url='login')
def enroll_course(request, pk):
    course = Course.objects.get(id=pk)
    student = Student.objects.get(user__id=request.user.id)
    student.courses.add(course)
    return redirect('home')



def approvals(request):
    users=User.objects.all().filter(is_active=False, is_teacher=True)
    context = {"users":users}
    return render(request, 'approvals.html', context)


def all_courses(request):
    courses = Course.objects.all()
    current_user = User.objects.filter(id=request.user.id)
    context = {"courses":courses, 'current_user':current_user}
    return render(request, 'all_courses.html', context)



def logout_user(request):
    logout(request)
    return redirect('home')