from django.db import models
class Members(models.Model):
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    cnfpassword = models.CharField(max_length = 255)
    fullname = models.CharField(max_length = 255)
    dob = models.DateField()
    num = models.CharField(max_length = 15)
    gender = models.CharField(max_length = 15) 