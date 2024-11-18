from django.db import models
from django.utils import timezone
from Candidates.models import Candidate
from Recruiters.models import Recruiter

class JobOffer(models.Model):
    """
    Model representing a job offer.
    """
    Id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, help_text="Name of the job offer")
    description = models.CharField(max_length=255, null=False, help_text="Description of the job offer")
    workTime = models.CharField(max_length=255, null=True, help_text="Work time for the job offer")
    location = models.CharField(max_length=255, null=True, help_text="Location of the job offer")
    expirationDate = models.DateTimeField(null=True, help_text="Expiration date of the job offer")
    salary = models.IntegerField(null=True, help_text="Salary for the job offer")
    skills = models.CharField(max_length=255, null=True, help_text="Skills required for the job offer")
    company = models.CharField(max_length=255, null=True, help_text="Company offering the job")
    email = models.CharField(max_length=255, null=True, help_text="Contact email for the job offer")
    numtel = models.CharField(max_length=255, null=True, help_text="Contact phone number for the job offer")
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, default=1, help_text="Recruiter offering the job")
    candidate_application = models.ManyToManyField(Candidate, related_name='applications', through='Application')
    candidate_match = models.ManyToManyField(Candidate, related_name='matches', through='Match')

class Application(models.Model):
    """
    Model representing a job application.
    """
    Id = models.AutoField(primary_key=True, editable=False)
    candidate_score = models.FloatField(null=True, help_text="Score of the candidate for the job application")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, help_text="Candidate applying for the job")
    jobOffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, help_text="Job offer being applied for")
    created_at = models.DateTimeField(default=timezone.now, help_text="Date and time when the application was created")

class Match(models.Model):
    """
    Model representing a match between a candidate and a job offer.
    """
    Id = models.AutoField(primary_key=True, editable=False)
    candidate_score = models.FloatField(null=True, help_text="Score of the candidate for the job match")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, help_text="Candidate matched with the job offer")
    jobOffer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, help_text="Job offer matched with the candidate")
    matchedSkills = models.CharField(max_length=255, null=True, help_text="Skills matched between the candidate and the job offer")

class Notification(models.Model):
    """
    Model representing a notification.
    """
    content = models.TextField(help_text="Content of the notification")
    read_status = models.BooleanField(default=False, help_text="Read status of the notification")
    created_at = models.DateTimeField(default=timezone.now, help_text="Date and time when the notification was created")
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='notifications', help_text="Recruiter receiving the notification")
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, help_text="Job offer related to the notification")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, help_text="Candidate related to the notification")

    def __str__(self):
        return f"Notification for {self.recruiter.name} about {self.job_offer.name}"