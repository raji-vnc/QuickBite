from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from accounts.views import profile_page
from restaurants.views  import home,menu_page,restaurant_settings,toggle_favourite,favourite_list,search,analytics_dashboard
# from orders.views import add_to_cart
from restaurants.views import restaurant_dashboard,manage_menu,add_category,add_item,manage_orders,accept_order,update_order_status,add_review
from orders.views import cart_page,update_cart_quantity,remove_from_cart,checkout_page,track_order,order_success,order_history,cart_count_api,apply_coupon,get_notifiaction
from delivery.views import rider_dashboard, pick_order, deliver_order,get_rider_location
from restaurants.views import approval_list, approve_restaurant, reject_restaurant
from restaurants.views import live_search



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('api/',include('api.urls')),
    path('', home, name='home'),
    path("api/rider-location/<int:order_id>/", get_rider_location, name="get_rider_location"),



path('cart/', cart_page, name='cart_page'),
path('cart/update/<int:cart_item_id>/<str:action>/', update_cart_quantity, name='update_cart_quantity'),
path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
path('order/track/<int:order_id>/', track_order, name='track_order'),
path('checkout/', checkout_page, name='checkout'),
path('order/success/<int:order_id>/', order_success, name='order_success'),
path('restaurant/dashboard/', restaurant_dashboard, name='restaurant_dashboard'),
path('restaurant/category/add/', add_category, name='add_category'),
path('restaurant/<int:restaurant_id>/menu/', menu_page, name='menu_page'),
    # path('add-to-cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
path('restaurant/menu/manage/',manage_menu, name='manage_menu'),
path('restaurant/item/add/', add_item, name='add_item'),
path('restaurant/orders/', manage_orders, name='manage_orders'),
path('restaurant/order/accept/<int:order_id>/', accept_order, name='accept_order'),
path('restaurant/order/update/<int:order_id>/<str:new_status>/', update_order_status, name='update_order_status'),
path('search/', search, name='search'),


path('rider/dashboard/', rider_dashboard, name='rider_dashboard'),
path('rider/order/pick/<int:order_id>/', pick_order, name='pick_order'),
path('rider/order/deliver/<int:order_id>/', deliver_order, name='deliver_order'),
path('profile/', profile_page, name='profile'),
path('orders/history/', order_history, name='order_history'),
path('review/add/<int:item_id>/', add_review, name='add_review'),
path('restaurant/settings/', restaurant_settings, name='restaurant_settings'),
path('restaurant/favourite/<int:restaurant_id>/', toggle_favourite, name='toggle_favourite'),
path('favourites/', favourite_list, name='favourite_list'),
path('restaurant/analytics/', analytics_dashboard, name='analytics_dashboard'),
path('api/cart/count/', cart_count_api, name='cart_count_api'),

path('admin/restaurant/approvals/', approval_list, name='restaurant_approval_list'),
path('admin/restaurant/approve/<int:id>/', approve_restaurant, name='approve_restaurant'),
path('admin/restaurant/reject/<int:id>/', reject_restaurant, name='reject_restaurant'),
path("apply-coupon/", apply_coupon, name="apply_coupon"),
path("api/notifications/", get_notifiaction, name="get_notifications"),
path("live-search/", live_search, name="live_search"),
path("restaurant/<int:restaurant_id>/review/", add_review, name="add_review"),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)