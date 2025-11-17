from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES=(
        ('customer','Customer'),
        ('restaurant','Restaurant'),
        ('rider','Rider'),
    )
    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default='customer')
    phone=models.CharField(max_length=15,blank=True,null=True)
    address=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.username

