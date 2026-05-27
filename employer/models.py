from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=10)
    lastname = models.CharField(max_length=10)
    email_id = models.EmailField()
    company = models.CharField(max_length=20)
    contact = models.CharField(max_length=10)
    image = models.ImageField()
    gender = models.CharField(max_length=10)


