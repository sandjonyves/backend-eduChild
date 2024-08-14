from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from account.models import Parent
# from django.contrib.gis.db import models
# Create your models here.



class Child(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    # name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    dateOfBirth = models.DateField()
    # lastKnownLocation=models.PointField(null=True,blank=True)
    lastLocationUpdate = models.DateTimeField(null=True, blank=True)
    parentUID = models.ForeignKey(Parent,on_delete=models.CASCADE,related_name='child')
    #  - lastLocationUpdate : timestamp

