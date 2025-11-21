from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from .models import CartItem
from restaurants.models import Item
from .models import CartItem,Item
from django.views.decorators.http import require_POST
from django.conf import settings
import razorpay
from orders.models import Order,OrderItem
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Order,Coupon
from django.http import JsonResponse
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from .models import Notification
def cart_page(request):
    cart_items=CartItem.objects.filter(user=request.user)
    total=sum([item.total_price() for item in cart_items])
    return render(request,'cart/cart.html',{
        "cart_items":cart_items,
        "total":total
    })


def update_cart_quantity(request,cart_item_id,action):
    item=get_list_or_404(CartItem,id=cart_item_id)
    if request.method=="POST":
        if action =="increase":
            item.quantity +=1
        elif action =="decrease" and item.quantity>1:
            item.quantity -=1
        item.save()

    return redirect('cart_page')

def remove_from_cart(request,cart_item_id):
    item=get_list_or_404(CartItem,id=cart_item_id)
    
    if request.method =="POST":
        item.delete()
    return redirect('cart_page')


def checkout_page(request):
    cart_items=CartItem.objects.filter(user=request.user)
    total=sum([item.total_price() for item in cart_items])

    if not cart_items:
        return redirect("cart_page")
    client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
    razorpay_order=client.order.create({
        'amount':cart_items,
        'total':total,
        'razorpay_key':settings.RAZORPAY_KEY_ID,
        'razorpay_order_id':razorpay_order['id'],
        'total_in_paise':int(total*100),
        'quickbite_order_id':Order.id,
    })


def track_order(request,order_id):
    order=get_list_or_404(Order,id=order_id,user=request.user)
    return render(request,"order_tracking/order_tracking.html",{'order':order})

def order_success(request,order_id):
    order=get_list_or_404(Order,id=order_id,user=request.user)
    return render(request, 'order_success/order_success.html',{"order":order})


@login_required
def order_history(request):
    orders=Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request,"order_success/order/order_history.html",{"orders":orders})

@require_POST
def add_to_cart(request,item_id):
    item=get_object_or_404(Item,id=item_id)

    if request.user.is_authenticated:
        cart_item,created=CartItem.objects.get_or_create(user=request.user,item=item)
        if not created:
            cart_item.quantity+=1
            cart_item.save()
        else:
            session_cart=request.session.get('cart',{})
            session_cart[str(item_id)]=int(session_cart.get(str(item_id),0)) + 1
            request.session['cart']=session_cart
            request.session.modified=True
        cart_count=get_cart_count_for_user(request)
        is_ajax=request.headers.get('x-requested-with')=='XMLHttpRequest'
        if is_ajax:
            return JsonResponse({'success':True,'cart_count':cart_count})

    return redirect(request.META.get('HTTP_REFERER','cart_page'))


def cart_count_api(request):
    if request.user.is_authenticated:
        cart_count=get_cart_count_for_user(request)
        count=CartItem.objects.filter(user=request.user).aggregate(total=models.Sum('quantity'))['total'] or 0

    else:
        session_cart=request.session.get('cart',{})
        count=sum(int(q) for q in session_cart.values()) if session_cart else 0
    return JsonResponse({'cart_count':cart_count})


def get_cart_count_for_user(request):
    if request.user.is_authenticated:
        total=CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    else:
        session_cart=request.session.get('cart',{})
        total = sum(int(q) for q in session_cart.values()) if session_cart else 0
        return int(total)
    
def apply_coupon(request):
    code=request.POST.get('coupon_code')
    total=float(request.POST.get('total_amount'))

    try:
        coupon=Coupon.objects.get(code__iexact=code,is_active=True)
        if coupon.expiry_date<timezone.now().date():
            return JsonResponse({"success":False,"message":"Coupon expired."})
        if total< coupon.min_amount:
            return JsonResponse({"success":False,"message":f"Minimum order₹{coupon.min_amount}required."})
        if coupon.discount_type=="percent":
            discount=coupon.discount_value
        final_amount=max(total-discount,0)
        return JsonResponse({
            "success":True,
            "discount":round(discount,2),
            "final_amount":round(final_amount,2)
                            })
    except Coupon.DoesNotExist:
        return JsonResponse({"duccess":False,"message":"Invalid coupon code."})
    
def get_notifiaction(request):
    if not request.user.is_authenticated:
        return JsonResponse({"notifications":[]})
    notifs=Notification.objects.filter(user=request.user,is_read=False)
    data=[
        {
            "id":n.id,
            "message":n.message,
            "time":n.created_at.strtime("%I:%M %p")
        }
        for n in notifs
    ]
    notifs.updated(is_read=True)
    return JsonResponse({"notifications":data})