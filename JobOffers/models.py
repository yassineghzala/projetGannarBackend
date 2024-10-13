from django.db import models

from Candidates.models import Candidate
from Recruiters.models import Recruiter

# Create your models here.
class JobOffer(models.Model):
    Id = models.AutoField(primary_key=True, editable=False,null=False)
    details = models.CharField(max_length=255,null=False)
    recruiter = models.ForeignKey(Recruiter,on_delete=models.CASCADE)
    candidate_application = models.ManyToManyField(Candidate, related_name='applications', through='Application')
    candidate_match = models.ManyToManyField(Candidate, related_name='matches', through='Match')



class Application(models.Model):
    Id = models.AutoField(primary_key=True, editable=False)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    jobOffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)



class Match(models.Model):
    Id = models.AutoField(primary_key=True, editable=False)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    jobOffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)