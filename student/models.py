from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class StudentProfile(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email_id = models.EmailField()
    contact = models.CharField(max_length=20)
    image = models.ImageField()
    gender = models.CharField(max_length=20)
    skills = models.CharField(max_length=200)
    resume = models.FileField()
    location = models.CharField(max_length=20)
    language = models.CharField(max_length=200)

    def resumename(self):
        return os.path.basename(self.resume.name)



class Education(models.Model):

    EDUCATION_CHOICES = [
        ('10th', '10th'),
        ('12th', '12th'),
        ('Graduation', 'Graduation'),
        ('Post Graduation', 'Post Graduation'),
    ]

    studuser = models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
    education_type = models.CharField(max_length=30,choices=EDUCATION_CHOICES)
    degree = models.CharField(max_length=200,blank=True,null=True)
    school_college = models.CharField(max_length=200,blank=True,null=True)
    board_university = models.CharField(max_length=200,blank=True,null=True)
    specialization = models.CharField(max_length=200,blank=True,null=True)
    passing_year = models.DateField(null=True, blank=True)
    marks = models.CharField(max_length=20,null=True, blank=True)



class Experience(models.Model):
    stud = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=50,blank=True,null=True)
    company_name = models.CharField(max_length=50,blank=True,null=True)
    startdate = models.DateField()
    enddate = models.DateField()
    salary = models.FloatField()
    job_profile = models.TextField()


