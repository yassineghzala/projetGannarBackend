from django.db import models

# Create your models here.
class Recruiter(models.Model):
    Id = models.AutoField(primary_key=True, editable=False,null=False)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    
    