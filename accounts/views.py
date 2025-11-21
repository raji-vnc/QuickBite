from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import UserRegisterForm,LoginForm
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from restaurants.models import Restaurant
def signup_view(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST)

        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role='customer'
            user.save()

            messages.success(request,"Account created succesfully")
            return redirect('login_view')
        
        else:
          form=UserRegisterForm()
    else:
        form=UserRegisterForm()

    return render(request,'accounts/signup.html',{'form':form})


def login_view(request):
    if request.method=="POST":
        form=LoginForm(request,data=request.POST)

        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')

            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,"Invalid credentials")
    else:
        form=LoginForm()
    return render(request,'accounts/login.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('login_view')

def restaurant_login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(username=username,password=password)
        if user and user.role =='restaurant':
            login(request,user)
            return redirect('restaurant_dashboard')
        else:
            messages.error(request,"invalid credentials or Not a Restaurant Account")
    return render(request,'accounts/restaurant_login.html')
    
def rider_login(request):
    if request.method=="POST":
        username=request.POSt.get("username")
        password=request.POST.get("password")

        user=authenticate(username=username,password=password)
        if user and user.role=="rider":
            login(request,user)
            return redirect('rider_dashboard')
        else:
            messages.error(request,"invalid credentials or not a Rider account")
        return render(request,"accounts/rider_login.html")
    
@login_required
def profile_page(request):
    user=request.user

    if request.method =="POST":
        user.email=request.POST.get("email")
        user.phone=request.POST.get("phone")
        user.address=request.POST.get("address")
        user.save()
        return redirect("profile")
    return render(request,"profile/profile.html",{"user":user})


User=get_user_model()

def restaurant_signup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get("email")
        password=request.POST.get('password')

        name=request.POST.get('name')
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        logo=request.FILES.get("logo")
        user=User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role='restaurant'
         )
        restaurant=Restaurant.objects.create(
        owner=user,
        name=name,
        address=address,
        phone=phone,
        logo=logo,
        is_approved=False
    )   
    
        messages.success(request,"signup successfull please wait for admin approval")
        return redirect('restaurant_login')
    return render(request,"accounts/restaurant_signup.html")


