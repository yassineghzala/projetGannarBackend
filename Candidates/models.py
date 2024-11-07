from django.db import models
from django.contrib.auth.models import AbstractUser , Group, Permission

# Create your models here.
class Resume(models.Model):
    Id = models.AutoField(primary_key=True, editable=False)
    file = models.FileField(upload_to="Resumes") 
    skills = models.CharField(max_length=255,null=True)

class Candidate(AbstractUser):
    id = models.AutoField(primary_key=True, editable=False)
    username = models.CharField(max_length=255,null=False,unique=True)
    email = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    cv = models.OneToOneField(Resume,on_delete=models.CASCADE,null=True) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
