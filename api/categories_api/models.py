from django.db import models

# Create your models here.


class Category(models.Model):
    
    serial = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=50,unique=True)
    category_url = models.CharField(max_length=300,unique=False,blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    # def __str__(self):
    #     return self

