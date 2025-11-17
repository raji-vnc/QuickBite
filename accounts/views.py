from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import UserRegisterForm,LoginForm
from .models import User


def signup_view(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST)

        if form.is_valid():
            user=form.save(comit=False)
            user.set_password(form.cleaned_data['password'])
            user.role='customer'
            user.save()
            messages.success(request,"Account created succesfully")
            return redirect('login_view')
        
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