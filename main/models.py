from django.db import models

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    student_id = models.CharField(max_length=7, unique=True)
    lrn = models.CharField(max_length=12, unique=True)
    lastname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100, blank=True)
    degree = models.CharField(max_length=100)
    year_level = models.IntegerField()
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=11)

    class Meta:
        ordering = ['lastname', 'firstname']

    def __str__(self):
        return f"{self.student_id} - {self.lastname}, {self.firstname}"
