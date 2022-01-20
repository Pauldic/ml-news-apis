from django.db import models
from rest_framework import serializers 
from django.contrib.postgres.fields import ArrayField
from users_api.models import UserProfile
import datetime
# Create your models here.


class News(models.Model):
    id = models.BigAutoField(primary_key=True,unique=True)
    link = models.CharField(max_length=500,unique=True)
    source = models.CharField(max_length=50,unique=False)
    author = models.CharField(max_length=100,unique=False,null=True)
    title = models.CharField(max_length=500,unique=False)
    small_description = models.TextField(unique=False, null=True)
    description = models.TextField(unique=False)
    category = models.CharField(max_length=500,unique=False)
    url = models.CharField(max_length=500,unique=False)
    urltoimage = models.CharField(max_length=500,unique=False,null=True)
    publishedat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now_add=True)
    entities = models.JSONField(default=dict,blank=True)
    tags = ArrayField(models.TextField())

    liked = models.PositiveIntegerField(default=0)
    unliked = models.PositiveIntegerField(default=0)        
    expired = models.DateField(default=None, null=True, blank=True)

    user=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        db_table='news'
        ordering = ['-id']
