from rest_framework import viewsets
from restaurants.models import Restaurant,Category,Item
from .serializers import RestaurantSerializer,CategorySerializer,ItemSerializer,OrderSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from orders.models import CartItem
from orders.models import Order,OrderItem,CartItem
from django.db import transaction
import razorpay
from django.conf import settings
from rest_framework.views import APIView


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Restaurant.objects.filter(is_approved=True)
    serializer_class=RestaurantSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class=CategorySerializer

    def get_queryset(self):
        restaurant_id=self.kwargs['restaurant_id']
        return Category.objects.filter(restaurant_id=restaurant_id)
    
class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class=ItemSerializer

    def get_queryset(self):
        restaurant_id=self.kwargs['restaurant_id']
        return Item.objects.filter(category_restaurant_id=restaurant_id)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class=CategorySerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)
    
    def create(self,request,*args,**kwargs):
        item_id=request.data.get('item')
        quantity=int(request.data.get('quantity',1))

        cart_item,created=CartItem.objects.get_or_create(user=request.user,item_id=item_id)
        if not created:
            cart_item.quantity+=quantity
            cart_item.save()
            
        serializer=self.get_serializer(cart_item)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        instance=self.get_object()
        return Response({"message":"item removed from cart"},status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return  Order.objects.filter(user=self.user).order_by('-created_at')

    @transaction.atomic 
    def create(self,request,*args,**kwargs):
        user=request.user
        cart_items=CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"error":"Your cart is empty"},status=400)
        total_amount=sum([item.total_price() for item in cart_items])

        order=Order.objects.create(
            user=user,
            total_amount=total_amount,
            status="pending"
        )

        for item in cart_items:
            OrderItem.objects.create(order=order,item=item.item,quantity=item.quantity)
        cart_items.delete()

        serializer=self.get_serializer(order)
        return Response(serializer.data,status=201)
    
    

class PaymentView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        amount=request.data.get('amount')

        if not amount:
            return Response({"error":"amount is required"}, status=400)
        
        amount=int(float(amount)**100)

        client=razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET)
        )
    
        payment=client.order.create({
            'amount':amount,
            "currency":"INR",
            "payment_capture":1
        })
        return Response({
            "order_id":payment['id'],
            "amount":amount,
            "key":settings.RAZORPAY_KEY_ID
        })
    

class PaymentSuccessView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        payment_id=request.data.get('payment_id')
        order_id=request.data.get('order_id')
        quickbiite_order_id=request.data.get('quickbite_order_id')

        try:
            order=order.objects.get(id=quickbiite_order_id,user=request.user)
            order.payment_id=payment_id
            order.status='accepted'
            order.save()

            return Response({'message':"payment successfull"})
        except Order.DoesNotExist:
            return Response({"error":"Order not found"},status=404)