from django.db import models
from accounts.models import User
# from restaurants.models import Item

class Restaurant(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    address=models.TextField()
    logo=models.ImageField(upload_to='restaurant/')
    phone=models.CharField(max_length=15,null=True,blank=True)
    open_time=models.TimeField(null=True,blank=True)
    close_time=models.TimeField(null=True,blank=True)
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
    rating=models.FloatField(default=0)

    def __str__(self):
        return self.name
class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    restaurant=models.ForeignKey('restaurants.Restaurant',default=False,on_delete=models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    rating=models.IntegerField(choices=[(1,1),(2,2),(3,3),(4,4),(5,5)])
    comment=models.TextField(blank=True)
    image1=models.ImageField(upload_to='review_photos/',null=True,blank=True)
    image2=models.ImageField(upload_to='review_photos/',null=True,blank=True)
    image3=models.ImageField(upload_to='review_photos/',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name}- {self.rating}⭐"
    
class FavouritRestaurant(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)

    class Meta:
        unique_together=('user','restaurant')
    def __str__(self):
        return f"{self.user.username}❤️{self.restaurant.name}"