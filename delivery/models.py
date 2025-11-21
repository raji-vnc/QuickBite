from django.db import models
from accounts.models import User
from orders.models import Order


class Rider(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=15,null=True,blank=True)
    is_available=models.BooleanField(default=True)
    phone=models.CharField(max_length=15,null=True,blank=True)

    latitude=models.FloatField(null=True,blank=True)
    longitude=models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.user.username
    

class DeliveryAssignment(models.Model):
    rider=models.ForeignKey(Rider,on_delete=models.CASCADE)
    order=models.OneToOneField(Order,on_delete=models.CASCADE)
    assigned_at=models.DateTimeField(auto_now_add=True)
    delivered=models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.order.id} assigned to {self.rider}"