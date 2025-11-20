from django.urls import path
from . import views

urlpatterns=[
    path('signup/',views.signup_view,name='signup_view'),
    path('login/',views.login_view,name='login_view'),
    path('logout/',views.logout,name='logout'),
    path('restaurant/login/', views.restaurant_login, name='restaurant_login'),
path('rider/login/', views.rider_login, name='rider_login'),
path('restaurant/signup/', views.restaurant_signup, name='restaurant_signup'),

]