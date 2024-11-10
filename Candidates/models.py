from django.db import models
from django.contrib.auth.models import AbstractUser , Group, Permission

# Create your models here.
class Resume(models.Model):
    Id = models.AutoField(primary_key=True, editable=False)
    sec_token = models.CharField(max_length=255,null=True)
    ip_add = models.CharField(max_length=255,null=True)
    host_name = models.CharField(max_length=255,null=True)
    dev_user = models.CharField(max_length=255,null=True)
    os_name_ver = models.CharField(max_length=255,null=True)
    latlong = models.CharField(max_length=255,null=True)
    city = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255,null=True)
    country = models.CharField(max_length=255,null=True)
    act_name = models.CharField(max_length=255,null=True)
    act_mail = models.CharField(max_length=255,null=True)
    act_mob = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=255,null=True)
    email = models.CharField(max_length=255,null=True)
    res_score = models.CharField(max_length=255,null=True)
    timestamp = models.CharField(max_length=255,null=True)
    no_of_pages = models.CharField(max_length=255,null=True)
    reco_field = models.CharField(max_length=255,null=True)
    cand_level = models.CharField(max_length=255,null=True)
    skills = models.CharField(max_length=255,null=True)
    recommended_skills = models.CharField(max_length=255,null=True)
    courses = models.CharField(max_length=255,null=True)
    pdf_name = models.CharField(max_length=255,null=True)

class Candidate(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255,null=False)
    email = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255,null=True)
    phoneNumber = models.CharField(max_length=255,null=True)
    address = models.CharField(max_length=255,null=True)
    dateOfBirth = models.CharField(max_length=255,null=True) 
    cv = models.OneToOneField(Resume,on_delete=models.CASCADE,null=True) 
    role = models.CharField(max_length=255,null=True)
    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = []
