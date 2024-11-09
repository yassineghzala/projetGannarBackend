from django.db import models

# Create your models here.
class Recruiter(models.Model):
    id = models.AutoField(primary_key=True, editable=False,null=False)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255,null=True)
    company = models.CharField(max_length=255,null=True)
    companyAddress = models.CharField(max_length=255,null=True)
    post = models.CharField(max_length=255,null=True)
    domain = models.CharField(max_length=255,null=True)
    phoneNumber = models.CharField(max_length=255,null=True)

# class Notification(models.Model):
#     id = models.AutoField(primary_key=True, editable=False)
#     message = models.CharField(max_length=255,null=True)
#     date = models.DateTimeField(null=True)
#     recruiter = models.ForeignKey(Recruiter,on_delete=models.CASCADE,default=1)
    