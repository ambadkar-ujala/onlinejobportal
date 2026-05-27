from django.db import models
from employer.models import Employer
from student.models import StudentProfile

# Create your models here.

class Job(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    experience = models.CharField(max_length=200)
    skills = models.CharField(max_length=200)
    salary = models.FloatField()
    company_logo = models.ImageField(default='/images/aaa.jpeg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class JobDetails(models.Model):
    EMPLOYEE_CHOICES = (
        ('1', '1-50'),
        ('2', '51-200'),
        ('3', '201-500'),
        ('4', 'More than 500'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    job_requirements = models.TextField(max_length=200)
    job_responsibilities = models.TextField(max_length=200)
    no_of_employees = models.CharField(max_length=200, choices=EMPLOYEE_CHOICES)
    registration_no = models.CharField(max_length=200)
    company_info = models.TextField(max_length=200)
    company_address = models.CharField(max_length=200)


class Application(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    resume = models.FileField()

class SavedJob(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)