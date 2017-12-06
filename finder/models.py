from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserQuality(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)


class Resources(models.Model):
    name = models.CharField(max_length = 200)
    date_in = models.DateField('bekerulesi ido')
    date_out = models.DateField('kikerulesi ido')
    date_out.null = True
    date_out.blank = True


class ResourcesProper(models.Model):
    resources = models.ForeignKey(Resources, on_delete=models.CASCADE)
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200, default=None)


class UserResources(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.ForeignKey(Resources, on_delete=models.CASCADE)