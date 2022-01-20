from django.db import models
from rest_framework import serializers
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class UserProfile(models.Model):
    account_id = models.IntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=50, unique=False, null=True)
    last_name = models.CharField(max_length=50, unique=False, null=True)
    avatar_url = models.CharField(max_length=300, unique=False, blank=True,
                                  default="https://jeffjbutler.com/wp-content/uploads/2018/01/default-user.png")
    address = models.CharField(max_length=300, unique=False, blank=True)
    country = models.CharField(max_length=50, unique=False, blank=True)
    liked = ArrayField(models.IntegerField(blank=True, null=True), blank=True, null=True, default=list)
    unliked = ArrayField(models.IntegerField(blank=True, null=True), blank=True, null=True, default=list)
    read = ArrayField(models.IntegerField(blank=True, null=True), blank=True, null=True, default=list)
    interests = models.JSONField(default=dict, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + self.last_name
