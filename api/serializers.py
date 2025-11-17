from rest_framework import serializers
from orders.models import CartItem
from restaurants.models import Restaurant,Category,Item
from orders.models import Order,OrderItem

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model=Restaurant
        fields=['id','name','address','logo','phone']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields=['id','name','description','price','image','is_available','rating']



class CartItemSerializer(serializers.ModelSerializer):
    item_name=serializers.CharField(source='item.name',read_only=True)
    item_price=serializers.DecimalField(source='item.price',read_only=True,max_digits=10,decimal_places=2)
    item_image=serializers.ImageField(source='item.image',read_only=True)

    class Meta:
        model=CartItem
        fields=['id','item','item_name','item_price','item_image','quantity']    

class OrderItemSerializer(serializers.ModelSerializer):
    item_name=serializers.CharField('item.name',read_only=True)
    item_price=serializers.DecimalField(source='item.price',read_only=True,max_digits=10,decimal_places=2)

    class Meta:
        model=OrderItem
        fields=['id','item','item_name','item_price','quantity']

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,source='orderitem_set',read_only=True)
    status_display=serializers.CharField(source='get_status_dispaly',read_only=True)

    class Meta:
        model=Order
        fields=['id','total_amount','status_display','payment_id','created_at','items']