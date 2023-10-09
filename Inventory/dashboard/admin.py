from django.contrib import admin

# Register your models here.
from .models import Product,Order
from django.contrib.auth.models import Group

admin.site.site_header = "RAI-Inventory Dashboard"


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category','quantity')
    list_filter = ('category',)
    

admin.site.register(Order)
admin.site.register(Product,ProductAdmin)
#admin.site.unregister(Group)
