from django.db import models
from django.utils import timezone
from Candidates.models import Candidate
from Recruiters.models import Recruiter

# Create your models here.
class JobOffer(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True)
    description = models.CharField(max_length=255,null=False)
    workTime = models.CharField(max_length=255,null=True)
    location = models.CharField(max_length=255,null=True)
    expirationDate = models.DateTimeField(null=True)
    salary = models.IntegerField(null=True)
    skills = models.CharField(max_length=255,null=True)
    company = models.CharField(max_length=255,null=True)
    email = models.CharField(max_length=255,null=True)
    numtel = models.CharField(max_length=255,null=True)
    recruiter = models.ForeignKey(Recruiter,on_delete=models.CASCADE,default=1)
    candidate_application = models.ManyToManyField(Candidate, related_name='applications', through='Application')
    candidate_match = models.ManyToManyField(Candidate, related_name='matches', through='Match')



class Application(models.Model):
    Id = models.AutoField(primary_key=True, editable=False)
    candidate_score = models.FloatField(null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    jobOffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class Match(models.Model):
    Id = models.AutoField(primary_key=True, editable=False)
    candidate_score = models.FloatField(null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    jobOffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    matchedSkills = models.CharField(max_length=255, null=True) 


class Notification(models.Model):
    content = models.TextField()
    read_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='notifications')
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return f"Notification for {self.recruiter.name} about {self.job_offer.name}"    