from django.contrib import admin
from .models import Restaurant,Category,Item,Review,FavouritRestaurant

admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Review)
admin.site.register(FavouritRestaurant)
# @admin.register(Restaurant)
class Restaurant(admin.ModelAdmin):
    list_display=('name','owner','phone','is_approved')
    list_editable=('is_approved')