from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Rider,DeliveryAssignment
from orders.models import Order

@login_required
def rider_dashboard(request):
    rider=Rider.objects.get(user=request.user)
    assignments=DeliveryAssignment.objects.filter(rider=rider)
    orders=[a.order for a in assignments]
    return render(request,"rider/dashboard.html",{
        "rider":rider,
        "assignments":assignments,
        "orders":orders
    })
@login_required
def pick_order(request,order_id):
    assignment=DeliveryAssignment.objects.get(order_id=order_id)
    assignment.picked=True
    assignment.order.status="out_for _delivery"
    assignment.order.save()
    assignment.save()
    return redirect("rider_dashboard")

@login_required
def deliver_order(request,order_id):
    assignment=DeliveryAssignment.objects.get(order_id=order_id)
    assignment.delivered=True
    assignment.order.status="delivered"
    assignment.order.save()
    rider=assignment.rider
    rider.is_available=True
    rider.save()
    assignment.save()
    return redirect('rider_dashboard')