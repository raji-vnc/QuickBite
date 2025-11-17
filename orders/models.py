from django.db import models
from accounts.models import User
from restaurants.models import Item

class CartItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.item.price * self.quantity
    
    def __str__(self):
        return f"{self.item.name} x {self.quantity}"
    
ORDER_STATUS=(
    ('pending','Pending'),
    ('accepted','Accepted'),
    ('preparing','Preparing'),
    ('out_for_delivery','Out for Delivery'),
    ('delivered','Ddelivered'),
)
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=50,choices=ORDER_STATUS,default='pending')
    created_at=models.DateTimeField(auto_now_add=True)
    payment_id=models.CharField(max_length=150,blank=True,null=True)

    def __str__(self):
        return f"Order #{self.id}"
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"