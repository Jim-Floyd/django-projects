from tkinter import Widget
from django import forms
from django.forms import ModelForm
from django.db import transaction
from .models import Course, User, Student, Teacher
from django.contrib.auth.forms import UserCreationForm

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'description': forms.Textarea(attrs={'class':'form-control form-control-sm'}),
        }
    

class StudentSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'last_name': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            # 'password': forms.PasswordInput(attrs={'class':'form-control form-control-sm'}),
            'username': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'email': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
        }


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        return user


class TeacherSignUpForm(UserCreationForm):
    # password=forms.CharField(widget=forms.PasswordInput())
    # confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'last_name': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            # 'password': forms.PasswordInput(attrs={'class':'form-control form-control-sm'}),
            'username': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'email': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
        }
    
    # def clean(self):
    #     cleaned_data = super(TeacherSignUpForm, self).clean()
    #     password = cleaned_data.get("password")
    #     confirm_password = cleaned_data.get("confirm_password")

    #     if password != confirm_password:
    #         raise forms.ValidationError(
    #             "password and confirm_password does not match"
    #         )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.is_active = False
        user.save()
        teacher = Teacher.objects.create(user=user)
        return user