from django.db import models

from Recruiters.models import Recruiter

# Create your models here.
class JobOffer(models.Model):
    Id = models.IntegerField(primary_key=True,unique=True,null=False)
    details = models.CharField(max_length=255,null=False)
    recruiter = models.ForeignKey(Recruiter,on_delete=models.CASCADE)