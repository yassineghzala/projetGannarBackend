from django.db import models

from Candidates.models import Candidate
from Recruiters.models import Recruiter

# Create your models here.
class JobOffer(models.Model):
    Id = models.AutoField(primary_key=True, editable=False,null=False)
    name = models.CharField(max_length=255,null=True)
    description = models.CharField(max_length=255,null=False)
    workTime = models.CharField(max_length=255,null=True)
    location = models.CharField(max_length=255,null=True)
    salary = models.IntegerField(null=True)
    skills = models.CharField(max_length=255,null=True)
    recruiter = models.ForeignKey(Recruiter,on_delete=models.CASCADE)
    candidate_application = models.ManyToManyField(Candidate, related_name='applications', through='Application')
    candidate_match = models.ManyToManyField(Candidate, related_name='matches', through='Match')



class Application(models.Model):
    Id = models.AutoField(primary_key=True, editable=False)
    candidate_score = models.FloatField(null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    jobOffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)



class Match(models.Model):
    Id = models.AutoField(primary_key=True, editable=False)
    candidate_score = models.FloatField(null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    jobOffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)