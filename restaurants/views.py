from django.db.models import Q
from django.shortcuts import render,get_list_or_404,redirect,get_object_or_404
from django.contrib.auth.decorators  import login_required
from .models import Restaurant,Category,Item
from orders.models import Order,OrderItem
from django.db.models import Sum,Count
import datetime
from restaurants.models import Review,Restaurant,FavouritRestaurant
from delivery.utils import auto_assign_rider
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
def home(request):
    restaurants=Restaurant.objects.filter(is_approved=True)
    favourite_ids=[]
    if request.user.is_authenticated:
        favourite_ids=FavouritRestaurant.objects.filter(user=request.user).values_list("restaurant_id",flat=True)
    return render(request,'home/home.html',{'restuarants':restaurants,"favourite_ids":favourite_ids})

def menu_page(request,restaurant_id):
    restaurant=get_object_or_404(Restaurant,id=restaurant_id)
    categories=Category.objects.filter(restaurant=restaurant)

    current_cat=request.GET.get('category',"all")

    if current_cat =="all":
        items=Item.objects.filter(category__restaurant=restaurant)
    else:
        items=Item.objects.filter(category_id=current_cat)

    return render(request,'menu/menu.html',{
        "restuarant":restaurant,
        "categories":categories,
        "items":items,
        "current_ctegory":current_cat
            
    })

@login_required
def restaurant_dashboard(request):
    restaurant=Restaurant.objects.get(owner=request.user)
    return render(request,'restaurant/dashboard.html',{"restaurant":restaurant})

@login_required
def manage_menu(request):
    restaurant=Restaurant.objects.get(owner=request.user)
    items=Item.objects.filter(category_restaurant=restaurant)
    return render(request,'restaurant/manage.html',{"items":items})

@login_required
def add_category(request):
    restaurant=Restaurant.objects.get(owner=request.user)

    if request.method =="POST":
        name=request.POST.get("name")
        Category.objects.create(restaurant=restaurant,name=name)
        return redirect("manage_menu")
    return render(request,"restaurant/add_category.html")

@login_required
def add_item(request):
    restaurant=Restaurant.objects.get(owner=request.user)
    categories=Category.objects.filter(restaurant=restaurant)

    if request.method=="POST":
        category=Category.objects.get(id=request.POST.get("category"))
        Item.objects.create(
            category=category,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            image=request.FILES.get("image")
        )
        return redirect("manage_menu")
    return render(request,"restaurant/add_item.html",{"categories":categories})

@login_required
def manage_orders(request):
    restaurant=Restaurant.objects.get(owner=request.user)
    orders=Order.objects.filter(
        orderitem_item_category_restaurant=restaurant
    ).distinct().order_by('-created_at')

    return render(request,'restaurant/manage_orders.html',{"orders":orders})

@login_required
def accept_order(request,order_id):
    order=Order.objects.get(id=order_id)
    order.status="accepted"
    order.save()
    rider=auto_assign_rider(order)
    if rider:
        print("Rider Assigned",rider.user.username)
    else:
        print("No rider available")

    return redirect("manager_orders")

@login_required
def update_order_status(request,order_id,new_status):
    order=Order.objects.get(id=order_id)
    order.status=new_status
    order.save()
    return redirect("manage_orders")

@login_required
def add_review(request,item_id):
    if request.method=="POST":
        rating=request.POST.get("rating")
        comment=request.POST.get("comment")

        Review.objects.create(
            user=request.user,
            item_id=item_id,
            rating=rating,
            comment=comment
        )

        return redirect(request.META.get('HTTP_REFERER'))
    
@login_required
def add_review(request,item_id):
    if request.method=="POST":
        rating=int(request.POST.get("rating"))
        comment=request.POST.get("comment")

        Review.objects.create(
            user=request.user,
            item_id=item_id,
            rating=rating,
            comment=comment
        )
        item=Item.objects.get(id=item_id)
        reviews=item.review_set_all()
        item.avg_rating=sum(r.rating for r in reviews)/reviews.count()
        item.save()

        return redirect(request.META.GET('HTTP_REFERER'))
    
@login_required
def restaurant_settings(request):
    restaurant=Restaurant.objects.get(owner=request.user)

    if restaurant.method=="POST":
        restaurant.name=request.POST.get("name")
        restaurant.address=request.POST.get("address")
        restaurant.phone=request.POST.get("phone")
        restaurant.open_time=request.POST.get("open_time")
        restaurant.close_time=request.POST.get("close_time")

        if request.FILES.get("logo"):
            restaurant.logo=request.FILES.get("logo")
        restaurant.save()
        return redirect("restaurant_settings")
    return render(request,"restaurant/settings.html",{"restaurant":restaurant})


@login_required
def toggle_favourite(request,restaurant_id):
    fav=FavouritRestaurant.objects.filter(
        user=request.user,
        restaurant_id=restaurant_id
    ).first()
    if fav:
        fav.delete()
    else:
        FavouritRestaurant.objects.create(
            user=request.user,restaurant_id=restaurant_id
        )
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def favourite_list(request):
    favourites=FavouritRestaurant.objects.filter(user=request.user)
    return render(request,"favourite/favourite.html",{"favourites":favourites})

def search(request):
    query=request.GET.get("q","")
    restaurants=Restaurant.objects.filter(
        Q(name__icontains=query) | 
        Q(address__icontains=query) |
        Q(category__name__icontains=query)
    )

    items=Item.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )

    return render(request,"search/search_results.html",{
        "query":query,
        "restaurants":restaurants,
        "items":items
            
                })

@login_required
def analytics_dashboard(request):
    restaurant=Restaurant.objects.get(owner=request.user)
    items=restaurant.category_set.values_list('item__id',flat=True)
    order_items=OrderItem.objects.filter(item_id__in=items)
    total_orders = order_items.values("order").distinct().count()

    total_revenue=order_items.aggregate(
        total=Sum('price')
    )['total'] or 0

    last_7_days=[]
    day_labels=[]
    today=datetime.date.today()

    for i in range(7):
        day=today - datetime.timedelta(day=i)
        count=order_items.filter(order__created_at__date=day).count()
        last_7_days.append(count)
        day_labels.append(day.strftime("%b %d"))

    last_7_days.reverse()
    day_labels.reverse()

    top_items=order_items.values("item__name").annotate(
        total_sold=Sum("quantity")

    ).order_by("-total_sold")[:5]

    return render(request,"restaurant/analytics.html",{
        "total_orders":total_orders,
        "total_revenue":total_orders,
        "day_labels":day_labels,
        "last_7_days":last_7_days,
        "top_items":top_items

    })

@staff_member_required
def approval_list(request):
    pending=Restaurant.objects.filter(is_approved=False)
    return render(request,"admin/restaurant_approval.html",{
        'pending':pending
    })

@staff_member_required
def approve_restaurant(request,id):
    r=Restaurant.objects.get(id=id)
    r.is_approved=True
    r.save()
    return redirect('restaurant_approval_list')

@staff_member_required
def reject_restaurant(request,id):
    Restaurant.objects.get(id=id).delete()
    return redirect('restaurant_approval_list')


def live_search(request):
    query=request.GET.get("q","").strip()
    if query=="":
        return JsonResponse({"results":[]})
    
    restaurants=Restaurant.objects.filter(
        Q(name__icontains=query),
        is_approved=True
    )[:5]

    items=Item.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )[:5]

    results=[]

    for r in restaurants:
        results.append({
            "type":"item",
            "name":r.name,
            "id":r.id
        })
    for i in items:
        results.append({
            "type":"item",
            "name":i.name,
            "restaurant_id":i.category.restaurant.id
        })
    return JsonResponse({"results":results})
def add_review(request,restaurant_id):
    if request.method== "POST":
        rating=request.POST.get("rating")
        comment=request.POST.get("comment")

        image1=request.FILES.get('image1')
        image2=request.FILES.get("image2")
        image3=request.FILES.get("image3")
    Review.objects.create(
        user=request.user,
        restaurant_id=restaurant_id,
        rating=rating,
        image1=image1,
        image2=image2,
        image3=image3,
    )

    return redirect("restaurant_menu",restaurant_id=restaurant_id)
