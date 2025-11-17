from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet,CategoryViewSet,ItemViewSet,CartItemViewSet,OrderViewSet

router=DefaultRouter()
router.register(r'restaurants',RestaurantViewSet,basename='restaurants')
router.register(r'cart',CartItemViewSet,basename='cart')
router.register(r'orders',OrderViewSet,basename='orders')
urlpattererns=[
    path('',include(router.urls)),
    path('restaurants/<int:restaurant_id>/categories/',CategoryViewSet.as_view({
        'get':'list'
    }),name='restaurants-categories'),

   path('restaurants/<int:restaurant_id>/items/',ItemViewSet.as_view({'get':'list'}),name='restaurant-items'), 
    
]
