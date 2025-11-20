from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet,CategoryViewSet,ItemViewSet,CartItemViewSet,OrderViewSet,PaymentView,PaymentSuccessView

router=DefaultRouter()
router.register(r'restaurants',RestaurantViewSet,basename='restaurants')
router.register(r'cart',CartItemViewSet,basename='cart')
router.register(r'orders',OrderViewSet,basename='orders')
urlpatterns=[
    path('',include(router.urls)),
    path('restaurants/<int:restaurant_id>/categories/',CategoryViewSet.as_view({
        'get':'list'
    }),name='restaurants-categories'),

   path('restaurants/<int:restaurant_id>/items/',ItemViewSet.as_view({'get':'list'}),name='restaurant-items'), 

       path('payment/create/', PaymentView.as_view(), name='payment-create'),
    path('payment/success/', PaymentSuccessView.as_view(), name='payment-success'),

]
