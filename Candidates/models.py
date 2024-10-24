from django.db import models

# Create your models here.
class Resume(models.Model):
    Id = models.AutoField(primary_key=True, editable=False)
    file = models.FileField(upload_to="Resumes") 
    skills = models.CharField(max_length=255,null=True)

class Candidate(models.Model):
    Id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    cv = models.OneToOneField(Resume,on_delete=models.CASCADE,null=True) 


