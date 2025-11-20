from .models import CartItem
from django.db import models

def cart_count(request):
    count = CartItem.objects.filter(user=request.user).aggregate(
        total=models.Sum('quantity')
    )['total'] or 0

    return {'cart_count': count}  


