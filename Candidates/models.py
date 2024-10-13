from django.db import models



# Create your models here.
class Candidate(models.Model):
    Id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)



