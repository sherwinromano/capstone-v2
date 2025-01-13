from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.CharField(max_length=20, unique=True)
    lrn = models.CharField(max_length=12)
    degree = models.CharField(max_length=100)
    year_level = models.CharField(max_length=20)
    section = models.CharField(max_length=1, choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    ])
    sex = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    contact_number = models.CharField(max_length=11)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
