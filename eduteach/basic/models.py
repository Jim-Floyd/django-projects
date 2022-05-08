from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



class Course(models.Model):
    name = models.CharField(max_length = 40)
    description = models.TextField()
    price = models.FloatField()
    created_by = models.ForeignKey('User', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['name']

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    courses = models.ManyToManyField(Course, related_name='student')
    

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)




