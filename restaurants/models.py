from django.db import models
from accounts.models import User

class Restaurant(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    address=models.TextField()
    logo=models.ImageField(upload_to='restaurant/')
    phone=models.CharField(max_length=15,null=True,blank=True)
    is_approved=models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Category(models.Model):
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}-{self.restaurant.name}"

class Item(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    description=models.TextField(blank=True,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='items/')
    is_available=models.BooleanField(default=True)
    rating=models.FloatField(default=4.5)

    def __str__(self):
        return self.name